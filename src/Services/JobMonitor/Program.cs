﻿namespace Microsoft.HpcAcm.Services.JobMonitor
{
    using System;
    using System.IO;
    using T = System.Threading.Tasks;
    using Microsoft.Extensions.Configuration;
    using Microsoft.Extensions.DependencyInjection;
    using Microsoft.HpcAcm.Common.Dto;
    using Microsoft.HpcAcm.Common.Utilities;
    using Microsoft.HpcAcm.Services.Common;
    using Microsoft.WindowsAzure.Storage;
    using Microsoft.WindowsAzure.Storage.Queue;
    using Microsoft.WindowsAzure.Storage.Table;

    class Program
    {
        protected Program() { }

        static void Main(string[] args)
        {
            using (ServerBuilder builder = BuildServer(args))
            {
                var server = builder.BuildAsync().GetAwaiter().GetResult();
                server.Start(builder.CancelToken);

                while (Console.In.Peek() == -1) { T.Task.Delay(1000).Wait(); }
                builder.Logger?.Information("Stop message received, stopping");

                builder.Stop();
            }
        }

        static ServerBuilder BuildServer(string[] args) => new ServerBuilder(args)
            .ConfigServiceCollection((svc, config, token) =>
            {
                svc.Configure<JobEventWorkerGroupOptions>(config.GetSection(nameof(JobEventWorkerGroupOptions)));
                svc.Configure<TaskItemSourceOptions>(config.GetSection(nameof(TaskItemSourceOptions)));
                svc.Configure<ScriptSynchronizerOptions>(config.GetSection(nameof(ScriptSynchronizerOptions)));
                svc.AddTransient<JobCanceler>();
                svc.AddTransient<JobDispatcher>();
                svc.AddTransient<JobFinisher>();
                svc.AddTransient<ClusrunJobHandler>();
                svc.AddTransient<DiagnosticsJobHandler>();
                svc.AddTransient<JobEventWorker>();

                svc.AddSingleton<IWorker, JobEventWorkerGroup>();
                svc.AddSingleton<IWorker, ScriptSynchronizer>();
            });
    }
}
