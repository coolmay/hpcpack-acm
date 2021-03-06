﻿namespace Microsoft.HpcAcm.Services.JobMonitor
{
    using Microsoft.HpcAcm.Common.Dto;
    using Microsoft.HpcAcm.Common.Utilities;
    using Microsoft.HpcAcm.Services.Common;
    using Microsoft.WindowsAzure.Storage.Queue;
    using Microsoft.WindowsAzure.Storage.Table;
    using Newtonsoft.Json;
    using System;
    using System.Collections.Generic;
    using System.Linq;
    using System.Text;
    using System.Threading;
    using T = System.Threading.Tasks;

    class JobDispatcher : JobActionHandlerBase
    {
        private (bool, string) FillData(IEnumerable<InternalTask> tasks, Job job)
        {
            // TODO: check circle
            var tasksDict = tasks.ToDictionary(t => t.Id);
            foreach (var t in tasks)
            {
                if (t.ParentIds != null)
                {
                    foreach (var parentId in t.ParentIds)
                    {
                        if (tasksDict.TryGetValue(parentId, out InternalTask p))
                        {
#pragma warning disable S1121 // Assignments should not be made from within sub-expressions
                            (p.ChildIds ?? (p.ChildIds = new List<int>())).Add(t.Id);
#pragma warning restore S1121 // Assignments should not be made from within sub-expressions
                        }
                        else
                        {
                            return (false, $"Task {t.Id}'s parent {parentId} not found.");
                        }
                    }
                }

                t.RemainingParentIds = t.ParentIds?.ToHashSet();
                t.JobId = job.Id;
                t.JobType = job.Type;
                t.RequeueCount = job.RequeueCount;
            }

            return (true, null);
        }


        public override async T.Task ProcessAsync(Job job, JobEventMessage message, CancellationToken token)
        {
            var jobTable = this.Utilities.GetJobsTable();

            if (job.State != JobState.Queued)
            {
                this.Logger.Error("The job {0} state {1} is not queued.", job.Id, job.State);
                return;
            }

            var dispatchResult = await this.JobTypeHandler.DispatchAsync(job, token);
            if (dispatchResult == null)
            {
                this.Logger.Error("The job {0} script doesn't generate any tasks", job.Id);
                await this.Utilities.UpdateJobAsync(job.Type, job.Id, j =>
                {
                    j.State = JobState.Failed;
                    j.TaskCount = 0;
                }, token, this.Logger);

                await this.Utilities.AddJobsEventAsync(job, $"The job {job.Id} script doesn't generate any tasks.", EventType.Alert, token);

                return;
            }

            var tasks = dispatchResult.Tasks;
            var allParentIds = new HashSet<int>(tasks.SelectMany(t => t.ParentIds ?? new List<int>()));
            var endingIds = tasks.Where(t => !allParentIds.Contains(t.Id)).Select(t => t.Id).ToList();

            var startTask = InternalTask.CreateFrom(job);
            startTask.Id = 0;
            startTask.CustomizedData = InternalTask.StartTaskMark;
            tasks.ForEach(t =>
            {
                if (t.ParentIds == null || t.ParentIds.Count == 0) t.ParentIds = new List<int>() { startTask.Id };
                t.ChildIds?.Clear();
            });

            var endTask = InternalTask.CreateFrom(job);
            endTask.Id = int.MaxValue;
            endTask.CustomizedData = InternalTask.EndTaskMark;
            endTask.ParentIds = endingIds;
            this.Logger.Information("Job {0} task {1} has {2} parent ids, {3}", job.Id, endTask.Id, endTask.ParentIds.Count, string.Join(",", endTask.ParentIds));

            tasks.Add(startTask);
            tasks.Add(endTask);

            var (success, msg) = this.FillData(tasks, job);
            if (!success)
            {
                this.Logger.Error(msg);

                await this.Utilities.FailJobWithEventAsync(
                    job,
                    msg,
                    token);

                return;
            }

            const int MaxChildIds = 1000;

            this.Logger.Information("Job {0} Converting {1} Tasks to Instances.", job.Id, tasks.Count);
            var taskInstances = tasks.Select(it =>
            {
                string zipppedParentIds = Compress.GZip(string.Join(",", it.ParentIds ?? new List<int>()));

                var childIds = it.ChildIds;
                childIds = childIds ?? new List<int>();
                childIds = childIds.Count > MaxChildIds ? null : childIds;

                return new Task()
                {
                    ChildIds = childIds,
                    ZippedParentIds = zipppedParentIds,
                    CommandLine = it.CommandLine,
                    CustomizedData = it.CustomizedData,
                    Id = it.Id,
                    JobId = it.JobId,
                    JobType = it.JobType,
                    Node = it.Node,
                    RequeueCount = it.RequeueCount,
                    State = string.Equals(it.CustomizedData, Task.StartTaskMark, StringComparison.OrdinalIgnoreCase) ? TaskState.Finished : TaskState.Queued,
                    MaximumRuntimeSeconds = Math.Min(it.MaximumRuntimeSeconds, 604799),
                };
            }).ToList();

            var childIdsContent = tasks
                .Where(it => (it.ChildIds?.Count ?? 0) > MaxChildIds)
                .Select(it => new
                {
                    it.Id,
                    it.JobId,
                    it.RequeueCount,
                    it.ChildIds,
                })
                .ToList();

            this.Logger.Information("Job {0} Converting {1} Tasks to TaskStartInfo.", job.Id, tasks.Count);
            var taskInfos = tasks.Select(it => new TaskStartInfo()
            {
                Id = it.Id,
                JobId = it.JobId,
                JobType = it.JobType,
                NodeName = it.Node,
                Password = it.Password,
                PrivateKey = it.PrivateKey,
                PublicKey = it.PublicKey,
                UserName = it.UserName,
                StartInfo = new ProcessStartInfo(it.CommandLine, it.WorkingDirectory, null, null, null, it.EnvironmentVariables, null, it.RequeueCount),
            }).ToList();

            this.Logger.Information("Job {0} Inserting {1} Tasks to Table.", job.Id, tasks.Count);
            var jobPartitionKey = this.Utilities.GetJobPartitionKey(job.Type, job.Id);
            await jobTable.InsertOrReplaceBatchAsync(token, taskInstances.Select(t => new JsonTableEntity(
                jobPartitionKey,
                this.Utilities.GetTaskKey(job.Id, t.Id, job.RequeueCount),
                t)).ToArray());

            if (childIdsContent.Select(cid => cid.Id).Distinct().Count() != childIdsContent.Count)
            {
                await this.Utilities.FailJobWithEventAsync(
                    job,
                    $"Duplicate task ids found.",
                    token);

                return;
            }

            this.Logger.Information("Job {0} Uploading {1} Tasks child ids content to blob.", job.Id, childIdsContent.Count);
            await T.Task.WhenAll(childIdsContent.Select(async childIds =>
            {
                var taskKey = this.Utilities.GetTaskKey(childIds.JobId, childIds.Id, childIds.RequeueCount);
                var childIdsBlob = await this.Utilities.CreateOrReplaceTaskChildrenBlobAsync(taskKey, token);

                var jsonContent = JsonConvert.SerializeObject(childIds.ChildIds);
                await childIdsBlob.UploadTextAsync(jsonContent, Encoding.UTF8, null, null, null, token);
            }));

            this.Logger.Information("Job {0} Inserting {1} TaskInfo to Table.", job.Id, taskInfos.Count);
            await jobTable.InsertOrReplaceBatchAsync(token, taskInfos.Select(t => new JsonTableEntity(
                jobPartitionKey,
                this.Utilities.GetTaskInfoKey(job.Id, t.Id, job.RequeueCount),
                t)).ToArray());

            this.Logger.Information("Job {0} updating job status.", job.Id);
            JobState state = JobState.Queued;
            await this.Utilities.UpdateJobAsync(job.Type, job.Id, j =>
            {
                state = j.State = (j.State == JobState.Queued ? JobState.Running : j.State);
                j.TaskCount = taskInstances.Count - 2;
                j.MaximumRuntimeSeconds = dispatchResult.ModifiedJob.MaximumRuntimeSeconds;
            }, token, this.Logger);

            await this.Utilities.AddJobsEventAsync(job, "Job started.", EventType.Information, token);

            var jobCancel = new JobEventMessage() { Id = job.Id, Type = job.Type, EventVerb = "cancel" };
            var jobEventQueue = this.Utilities.GetJobEventQueue();
            await jobEventQueue.AddMessageAsync(new CloudQueueMessage(JsonConvert.SerializeObject(jobCancel)), null, TimeSpan.FromSeconds(dispatchResult.ModifiedJob.MaximumRuntimeSeconds), null, null, token);
            this.Logger.Information("Create job timeout cancel message success.");

            if (state == JobState.Running)
            {
                this.Logger.Information("Job {0} Starting the job", job.Id);
                async T.Task addFirstTask()
                {
                    var taskCompletionQueue = await this.Utilities.GetOrCreateJobTaskCompletionQueueAsync(job.Id, token);
                    await taskCompletionQueue.AddMessageAsync(new CloudQueueMessage(
                        JsonConvert.SerializeObject(new TaskCompletionMessage() { JobId = job.Id, Id = 0, JobType = job.Type, RequeueCount = job.RequeueCount, ChildIds = startTask.ChildIds })),
                        null, null, null, null, token);
                };

                async T.Task addRunningJob()
                {
                    var runningJobQueue = this.Utilities.GetRunningJobQueue();
                    await runningJobQueue.AddMessageAsync(new CloudQueueMessage(
                        JsonConvert.SerializeObject(new RunningJobMessage() { JobId = job.Id, JobType = job.Type, RequeueCount = job.RequeueCount })),
                        null, null, null, null, token);
                };

                await T.Task.WhenAll(addFirstTask(), addRunningJob());
            }
        }
    }
}
