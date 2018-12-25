#v1.0.0

import sys, json, copy, numpy, time, math, uuid

INTEL_PRODUCT_URI = {
    'MPI': {
        '2019 Update 1'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14879/l_mpi_2019.1.144.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14881/w_mpi_p_2019.1.144.exe'
            },
        '2019'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13584/l_mpi_2019.0.117.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13586/w_mpi_p_2019.0.117.exe'
            },
        '2018 Update 4'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13741/l_mpi_2018.4.274.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13653/w_mpi_p_2018.4.274.exe'
            },
        '2018 Update 3'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13112/l_mpi_2018.3.222.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13065/w_mpi_p_2018.3.210.exe'
            },
        '2018 Update 2'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12748/l_mpi_2018.2.199.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12745/w_mpi_p_2018.2.185.exe'
            },
        '2018 Update 1'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mpi_2018.1.163.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12443/w_mpi_p_2018.1.156.exe'
            },
        '2018'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12120/l_mpi_2018.0.128.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12114/w_mpi_p_2018.0.124.exe'
            }
        },
    'MKL': {
        '2019 Update 1'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14895/l_mkl_2019.1.144.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/14893/w_mkl_2019.1.144.exe'
            },
        '2019'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13575/l_mkl_2019.0.117.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13558/w_mkl_2019.0.117.exe'
            },
        '2018 Update 4'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13725/l_mkl_2018.4.274.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13707/w_mkl_2018.4.274.exe'
            },
        '2018 Update 3'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13005/l_mkl_2018.3.222.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/13037/w_mkl_2018.3.210.exe'
            },
        '2018 Update 2'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12725/l_mkl_2018.2.199.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12692/w_mkl_2018.2.185.exe'
            },
        '2018 Update 1'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12414/l_mkl_2018.1.163.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12394/w_mkl_2018.1.156.exe'
            },
        '2018'.lower(): {
            'Linux': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12070/l_mkl_2018.0.128.tgz',
            'Windows': 'http://registrationcenter-download.intel.com/akdlm/irc_nas/tec/12079/w_mkl_2018.0.124.exe'
            }
        }
    }

HPC_DIAG_USERNAME = 'hpc_diagnostics'
HPC_DIAG_PASSWORD = 'p@55word'

def main():
    diagName, diagArgs, targetNodes, windowsNodes, linuxNodes, rdmaNodes, vmSizeByNode, tasks, taskResults = parseStdin()
    isMap = False if tasks and taskResults else True

    if diagName == 'MPI-Pingpong':
        arguments = {
            'Intel MPI version': '2018 Update 4',
            'Packet size': -1,
            'Mode': 'Tournament',
            'Debug': False
        }
        parseArgs(diagArgs, arguments)
        if isMap:
            return mpiPingpongMap(arguments, windowsNodes, linuxNodes, rdmaNodes)
        else:
            return mpiPingpongReduce(arguments, targetNodes, tasks, taskResults)

    if diagName == 'MPI-Ring':
        arguments = {
            'Intel MPI version': '2018 Update 4',
        }
        parseArgs(diagArgs, arguments)
        if isMap:
            return mpiRingMap(arguments, windowsNodes, linuxNodes, rdmaNodes)
        else:
            return mpiRingReduce(targetNodes, tasks, taskResults)
   
    if diagName.startswith('Prerequisite-Intel'):
        arguments = {
            'Version': '2018 Update 4',
            'Max runtime': 1800
        }
        parseArgs(diagArgs, arguments)
        product = 'MPI' if 'MPI' in diagName else 'MKL'
        if isMap:
            return installIntelProductMap(arguments, windowsNodes, linuxNodes, product)
        else:
            return installIntelProductReduce(arguments, tasks, taskResults, product)
    
    if diagName == 'Standalone Benchmark-Linpack':
        arguments = {
            'Intel MKL version': '2018 Update 4',
            'Size level': 10
        }
        parseArgs(diagArgs, arguments)
        if isMap:
            return benchmarkLinpackMap(arguments, windowsNodes, linuxNodes, vmSizeByNode)
        else:
            return benchmarkLinpackReduce(arguments, tasks, taskResults)

def parseStdin():
    stdin = json.load(sys.stdin)

    job = stdin['Job']
    targetNodes = job['TargetNodes']
    if not targetNodes:
        raise Exception('No node specified for running the job')
    if len(targetNodes) != len(set([node.lower() for node in targetNodes])):
        raise Exception('Duplicate name of nodes')
    diagName = '{}-{}'.format(job['DiagnosticTest']['Category'], job['DiagnosticTest']['Name'])
    diagArgs = job['DiagnosticTest']['Arguments']
    if diagArgs:
        diagArgs = [{key.lower():arg[key] for key in arg} for arg in diagArgs] # normalize the keys in arguments to lower case
        argNames = [arg['name'].lower() for arg in diagArgs]
        if len(argNames) != len(set(argNames)):
            raise Exception('Duplicate diagnostics arguments')

    nodes = stdin.get('Nodes')
    windowsNodes = linuxNodes = rdmaNodes = None
    vmSizeByNode = {}
    if nodes:
        missingInfoNodes = [node['Node'] for node in nodes if not node['NodeRegistrationInfo'] or not node['Metadata']]
        if missingInfoNodes:
            raise Exception('Missing infomation for node(s): {}'.format(', '.join(missingInfoNodes)))
        rdmaVmSizes = set([size.lower() for size in ['Standard_H16r', 'Standard_H16mr', 'Standard_A8', 'Standard_A9']])
        metadataByNode = {node['Node']:json.loads(node['Metadata']) for node in nodes}
        windowsNodes = set()
        linuxNodes = set()
        unknownNodes = set()
        rdmaNodes = set()
        for node in targetNodes:
            osType = metadataByNode[node]['compute']['osType']
            if osType.lower() == 'Windows'.lower():
                windowsNodes.add(node)
            elif osType.lower() == 'Linux'.lower():
                linuxNodes.add(node)
            else:
                unknownNodes.add(node)
            vmSize = metadataByNode[node]['compute']['vmSize']
            vmSizeByNode[node] = vmSize
            if vmSize.lower() in rdmaVmSizes:
                rdmaNodes.add(node)
        if unknownNodes:
            raise Exception('Unknown OS type of node(s): {}'.format(', '.join(unknownNodes)))

    tasks = stdin.get('Tasks')
    taskResults = stdin.get('TaskResults')
    if tasks and taskResults:
        if len(tasks) != len(taskResults):
            raise Exception('Task count {} is not equal to task result count {}'.format(len(tasks), len(taskResults)))
        taskIdNodeNameInTasks = set(['{}:{}'.format(task['Id'], task['Node']) for task in tasks])
        taskIdNodeNameInTaskResults = set(['{}:{}'.format(task['TaskId'], task['NodeName']) for task in taskResults])
        difference = (taskIdNodeNameInTasks | taskIdNodeNameInTaskResults) - (taskIdNodeNameInTasks & taskIdNodeNameInTaskResults)
        if difference:
            raise Exception('Task id and node name mismatch in "Tasks" and "TaskResults": {}'.format(', '.join(difference)))
        nodesInJob = set(targetNodes)
        tasksOnUnexpectedNodes = ['{}:{}'.format(task['Id'], task['Node']) for task in tasks if task['Node'] not in nodesInJob]
        if tasksOnUnexpectedNodes:
            raise Exception('Unexpected nodes in tasks: {}'.format(', '.join(tasksOnUnexpectedNodes)))

    return diagName, diagArgs, targetNodes, windowsNodes, linuxNodes, rdmaNodes, vmSizeByNode, tasks, taskResults

def parseArgs(diagArgsIn, diagArgsOut):
    if diagArgsIn:
        diagArgsMap = {key.lower():key for key in diagArgsOut}
        for arg in diagArgsIn:
            argName = arg['name'].lower()
            if argName in diagArgsMap:
                key = diagArgsMap[argName]
                argType = type(diagArgsOut[key])
                diagArgsOut[key] = argType(arg['value'])

def globalCheckIntelProductVersion(product, version):
    if product not in INTEL_PRODUCT_URI or version.lower() not in INTEL_PRODUCT_URI[product]:
        raise Exception('Intel {} {} is not supported'.format(product, version))

def globalGetDefaultInstallationLocationWindows(product, version):
    versionNumber = INTEL_PRODUCT_URI[product][version]['Windows'].split('_')[-1][:-len(".exe")]
    if versionNumber == '2018.4.274':
        versionNumber = '2018.5.274'        
    return 'C:\Program Files (x86)\IntelSWTools\compilers_and_libraries_{}\windows\{}'.format(versionNumber, product.lower())

def globalGetDefaultInstallationLocationLinux(product, version):
    versionNumber = INTEL_PRODUCT_URI[product][version]['Linux'].split('_')[-1][:-len(".tgz")]
    if versionNumber == '2018.4.274':
        versionNumber = '2018.5.274'        
    return '/opt/intel/compilers_and_libraries_{}/linux/{}'.format(versionNumber, product.lower())
    
SSH_PRIVATE_KEY = '''-----BEGIN RSA PRIVATE KEY-----
MIIEowIBAAKCAQEA06bdmM5tU/InWfakBnAltIA2WEvuZ/3qFwaT4EkmgJuEITxi+3NnXn7JfW+q
6ezBc4lx6J0EuPggDIcslbczyz65QrB2NoH7De1PiRtWNWIonQDZHTYCbnaU3f/Nzsoj62lgfkSf
Uj4Osxd0yHCuGsfCtKMDES3d55RMUdVwbrXPL8jUqA9zh4miV9eX0dh/+6pCqPD7/dnOCy/rYtXs
wgdjKG57O6eaT3XxiuozP00E5tZ7wF0fzzXBuA2Z21Sa2U42sOeeNuOvOuKQkrIzprhHhpDik31m
HZK47F7eF2i7j/0ImedOFdgA1ETPPKFLSGspvf1xbHgEgGz1kjFq/QIEAAEAAQKCAQABHZ2IW741
7RKWsq6J3eIBzKRJft4J7G3tvJxW8e3nOpVNuSXEbUssu/HUOoLdVVhuHPN/1TUgf69oXTtiRIVc
LIPNwcrGRGHwaP0JJKdY4gallLFMCB9i5FkhnJXbaiJvq+ndoqnnAPLf9GfVDqhV5Jqc8nxeDZ2T
ks037GobtfMuO5WeCyTAMzc7tDIsn0HGyV0pSa7JFHAKorUuBMNnjEM+SBL37AqwcVFkstC4YD3I
7j4miRE3loxPmBJs5HMTV4jpAGNbNmrPzfrmP4swHNoc9LR7YKpfzVpAzb24QY82fewvOxRZH6Hz
BVhueJZAGV62JbBeaw9eeujDp+UBAoGBAN6IanPN/wqdqQ0i5dBwPK/0Mcq6bNtQt6n8rHD/C/xL
FuhuRhLPI6q7sYPeSZu84EjyArLMR1o0GW90Ls4JzIxjxGCBgdUHG8YdmB9jNIjR5notYQcRNxaw
wLuc5nurPt7QaxvqO3JcaDbw9c6q9c7xNE3Wlak4xxKeiXsWyHQdAoGBAPN7hpqISKIc+8dPc5kg
uJDDPdFcJ8py0nbysEYtY+hUaDxfw7Cm8zrNj+M9BbQR9yM6EW16P0FQ+/0XBrLMVpRkyJZ0Y3Ij
5Qol5IxJPyWzfj6e7cd9Rkvqs2sQcBehXCbQHjfpB12yu3excQBPT0Lr5gei7yfc+D21hGWDH1xh
AoGAM2lm1qxf4O790HggiiB0FN6g5kpdvemPFSm4GT8DYN1kRHy9mbjbb6V/ZIzliqJ/Wrr23qIN
Vgy1V6eK7LUc2c5u3zDscu/6fbH2pEHCMF32FoIHaZ+Tj510WaPtJ+MvWkDijgd2hnxM42yWDZI3
ygC16cnKt9bTPzz7XEGuPA0CgYBco2gQTcAM5igpqiIaZeezNIXFrWF6VnubRDUrTkPP9qV+KxWC
ldK/UczoMaSE4bz9Cy/sTnHYwR5PKj6jMrnSVhI3pGrd16hiVw6BDbFX/9YNr1xa5WAkrFS9bJCp
fPxZzB9jOGdUEBfhr4KGEqbemHB6AVUq/pj4qaKJGP2KoQKBgFt7cqr8t+0zU5ko+B2pxmMprsUx
qZ3mBATMD21AshxWxsawpqoPJJ3NTScNrjISERQ6RG3lQNv+30z79k9Fy+5FUH4pvqU4sgmtYSVH
M4xW+aJnEhzIbE7a4an2eTc0pAxc9GexwtCFwlBouSW6kfOcMgEysoy99wQoGNgRHY/D
-----END RSA PRIVATE KEY-----'''

def mpiPingpongMap(arguments, windowsNodes, linuxNodes, rdmaNodes):
    mpiVersion = arguments['Intel MPI version']
    packetSize = arguments['Packet size']
    mode = arguments['Mode'].lower()
    globalCheckIntelProductVersion('MPI', mpiVersion)
    mpiInstallationLocationWindows = globalGetDefaultInstallationLocationWindows('MPI', mpiVersion)
    mpiInstallationLocationLinux = globalGetDefaultInstallationLocationLinux('MPI', mpiVersion)
    tasks = mpiPingpongCreateTasksWindows(list(windowsNodes & rdmaNodes), True, 0, mpiInstallationLocationWindows, packetSize)
    tasks += mpiPingpongCreateTasksWindows(list(windowsNodes - rdmaNodes), False, len(tasks) + 1, mpiInstallationLocationWindows, packetSize)
    tasks += mpiPingpongCreateTasksLinux(list(linuxNodes & rdmaNodes), True, len(tasks) + 1, mpiInstallationLocationLinux, mode, packetSize, None)
    tasks += mpiPingpongCreateTasksLinux(list(linuxNodes - rdmaNodes), False, len(tasks) + 1, mpiInstallationLocationLinux, mode, packetSize, None)
    print(json.dumps(tasks))

def mpiPingpongCreateTasksWindows(nodelist, isRdma, startId, mpiLocation, log):
    tasks = []
    if len(nodelist) == 0:
        return tasks

    mpiEnvFile = r'{}\intel64\bin\mpivars.bat'.format(mpiLocation)
    rdmaOption = ''
    taskLabel = '[Windows]'
    if isRdma:
        rdmaOption = '-env I_MPI_FABRICS=shm:dapl -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0'
        taskLabel += '[RDMA]'

    taskTemplate = {
        'UserName': HPC_DIAG_USERNAME,
        'Password': HPC_DIAG_PASSWORD,
        'EnvironmentVariables': {'CCP_ISADMIN': 1}
    }

    sampleOption = '-msglog {}:{}'.format(log, log + 1) if -1 < log < 30 else '-iter 10'
    commandSetFirewall = r'netsh firewall add allowedprogram "{}\intel64\bin\mpiexec.exe" hpc_diagnostics_mpi'.format(mpiLocation) # this way would only add one row in firewall rules
    # commandSetFirewall = r'netsh advfirewall firewall add rule name="hpc_diagnostics_mpi" dir=in action=allow program="{}\intel64\bin\mpiexec.exe"'.format(mpiLocation) # this way would add multiple rows in firewall rules when it is executed multiple times
    commandRunIntra = r'\\"%USERDOMAIN%\%USERNAME%`n{}\\" | mpiexec {} IMB-MPI1 pingpong'.format(HPC_DIAG_PASSWORD, rdmaOption)
    commandRunInter = r'\\"%USERDOMAIN%\%USERNAME%`n{}\\" | mpiexec {} -hosts [nodepair] -ppn 1 IMB-MPI1 -time 60 {} pingpong'.format(HPC_DIAG_PASSWORD, rdmaOption, sampleOption)
    commandMeasureTime = "$stopwatch = [system.diagnostics.stopwatch]::StartNew(); [command]; if($?) {'Run time: ' + $stopwatch.Elapsed.TotalSeconds}"

    idByNode = {}

    id = startId
    for node in nodelist:
        command = commandMeasureTime.replace('[command]', commandRunIntra)
        task = copy.deepcopy(taskTemplate)
        task['Id'] = id
        task['Node'] = node
        task['CommandLine'] = '{} && "{}" && powershell "{}"'.format(commandSetFirewall, mpiEnvFile, command)
        task['CustomizedData'] = '{} {}'.format(taskLabel, node)
        task['MaximumRuntimeSeconds'] = 30
        tasks.append(task)
        idByNode[node] = id
        id += 1

    if len(nodelist) < 2:
        return tasks

    taskgroups = mpiPingpongGetGroups(nodelist)
    for taskgroup in taskgroups:
        idByNodeNext = {}
        for nodepair in taskgroup:
            nodes = ','.join(nodepair)
            command = commandMeasureTime.replace('[command]', commandRunInter).replace('[nodepair]', nodes)
            task = copy.deepcopy(taskTemplate)
            task['Id'] = id
            task['Node'] = nodepair[0]
            task['CommandLine'] = '"{}" && powershell "{}"'.format(mpiEnvFile, command)
            task['ParentIds'] = [idByNode[node] for node in nodepair if node in idByNode]
            task['CustomizedData'] = '{} {}'.format(taskLabel, nodes)
            task['MaximumRuntimeSeconds'] = 60
            tasks.append(task)
            idByNodeNext[nodepair[0]] = id
            idByNodeNext[nodepair[1]] = id
            id += 1
        idByNode = idByNodeNext
    return tasks

def mpiPingpongCreateTasksLinux(nodelist, isRdma, startId, mpiLocation, mode, log, debugCommand):
    tasks = []
    if len(nodelist) == 0:
        return tasks

    rdmaOption = ''
    taskLabel = '[Linux]'
    if isRdma:
        rdmaOption = '-env I_MPI_FABRICS=shm:dapl -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0'
        taskLabel += '[RDMA]'

    scriptLocation = 'diagtestscripts'
    filterScriptDir = '/tmp/hpc_{}'.format(scriptLocation)
    filterScriptName = 'MPI-Pingpong-filter.py'
    filterScriptVersion = '#v0.12'
    filterScriptPath = '{}/{}'.format(filterScriptDir, filterScriptName)
    commandDownloadScript = 'if [ ! -f {0} ] || [ "`head -n1 {0}`" != "{1}" ]; then wget -P {2} ${{blobEndpoint}}{3}/{4} >stdout 2>stderr; fi && '.format(filterScriptPath, filterScriptVersion, filterScriptDir, scriptLocation, filterScriptName)
    commandParseResult = " && cat stdout | [parseResult] >raw && cat raw | tail -n +2 | awk '{print [columns]}' | tr ' ' '\n' | [parseValue] >data"
    commandGenerateOutput = " && cat data | head -n1 >output && cat data | tail -n1 >>output && cat timeResult >>output && cat raw >>output && cat output | python {}".format(filterScriptPath)
    commandGenerateError = ' || (errorcode=$? && echo "MPI Pingpong task failed!" >error && cat stdout stderr >>error && cat error && exit $errorcode)'
    commandLine = commandDownloadScript + "TIMEFORMAT='%3R' && (time timeout [timeout]s bash -c '[sshcommand] && source {0}/intel64/bin/mpivars.sh && [mpicommand]' >stdout 2>stderr) 2>timeResult".format(mpiLocation) + commandParseResult + commandGenerateOutput + commandGenerateError
    taskTemplateOrigin = {
        "Id":0,
        "CommandLine":commandLine,
        "Node":None,
        "UserName":HPC_DIAG_USERNAME,
        "Password":None,
        "PrivateKey":SSH_PRIVATE_KEY,
        "CustomizedData":None,
        "MaximumRuntimeSeconds":1000
    }

    headingStartId = startId
    headingNode2Id = {}
    taskStartId = headingStartId + len(nodelist)

    # Create task for every node to run Intel MPI Benchmark - PingPong between processors within each node.
    # Ssh keys will also be created by these tasks for mutual trust which is necessary to run the following tasks

    sshcommand = "rm -f ~/.ssh/known_hosts" # Clear ssh knownhosts
    checkcore = 'bash -c "if [ `grep -c ^processor /proc/cpuinfo` -eq 1 ]; then exit -10; fi"' # MPI Ping Pong can not get result but return 0 if core number is less than 2, so check core number and fail mpicommand if there is no result
    mpicommand = "mpirun -env I_MPI_SHM_LMT=shm {} IMB-MPI1 pingpong && {}".format(rdmaOption, checkcore)
    parseResult = "tail -n29 | head -n25"
    columns = "$3,$4"
    parseValue = "sed -n '1p;$p'"
    timeout = "600"
    taskTemplate = copy.deepcopy(taskTemplateOrigin)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[sshcommand]", sshcommand)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[mpicommand]", mpicommand)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[columns]", columns)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[parseResult]", parseResult)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[parseValue]", parseValue)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[timeout]", timeout)
    if debugCommand:
        taskTemplate["CommandLine"] = debugCommand

    id = headingStartId
    for node in nodelist:
        task = copy.deepcopy(taskTemplate)
        task["Id"] = id
        task["Node"] = node
        task["CustomizedData"] = '{} {}'.format(taskLabel, node)
        tasks.append(task)
        headingNode2Id[node] = id
        id += 1

    if len(nodelist) < 2:
        return tasks

    # Create tasks to run Intel MPI Benchmark - PingPong between all node pairs in selected nodes.

    if -1 < log < 30:
        sampleOption = "-msglog {}:{}".format(log, log + 1)
        parseResult = "tail -n 8 | head -n 3"
        parseValue = "tail -n2"
        timeout = 20
    else:
        sampleOption = "-iter 10"
        parseResult = "tail -n 29 | head -n 25"
        parseValue = "sed -n '1p;$p'"
        timeout = 20

    sshcommand = "host [pairednode] && ssh-keyscan [pairednode] >>~/.ssh/known_hosts" # Add ssh knownhosts
    mpicommand = "mpirun -hosts [dummynodes] {} -ppn 1 IMB-MPI1 -time 60 {} pingpong".format(rdmaOption, sampleOption)
    columns = "$3,$4"

    taskTemplate = copy.deepcopy(taskTemplateOrigin)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[sshcommand]", sshcommand)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[mpicommand]", mpicommand)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[columns]", columns)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[parseResult]", parseResult)
    taskTemplate["CommandLine"] = taskTemplate["CommandLine"].replace("[parseValue]", parseValue)

    if mode == "Parallel".lower():
        timeout *= 10
        taskTemplate["MaximumRuntimeSeconds"] = 300

    if mode == 'Tournament'.lower():
        taskgroups = mpiPingpongGetGroups(nodelist)
        id = taskStartId
        firstGroup = True
        for taskgroup in taskgroups:
            nodeToIdNext = {}
            for nodepair in taskgroup:
                task = copy.deepcopy(taskTemplate)
                nodes = ','.join(nodepair)
                task["Id"] = id
                task["Node"] = nodepair[0]
                task["ParentIds"] = [headingNode2Id[node] for node in nodepair] if firstGroup else [nodeToId[node] for node in nodepair if node in nodeToId]
                task["CommandLine"] = task["CommandLine"].replace("[dummynodes]", nodes)
                task["CommandLine"] = task["CommandLine"].replace("[pairednode]", nodepair[1])
                task["CommandLine"] = task["CommandLine"].replace("[timeout]", str(timeout))
                if debugCommand:
                    task["CommandLine"] = debugCommand
                task["CustomizedData"] = '{} {}'.format(taskLabel, nodes)
                tasks.append(task)
                nodeToIdNext[nodepair[0]] = id
                nodeToIdNext[nodepair[1]] = id
                id += 1
            firstGroup = False
            nodeToId = nodeToIdNext
    else:
        id = taskStartId
        nodepairs = []
        for i in range(0, len(nodelist)):
            for j in range(i+1, len(nodelist)):
                nodepairs.append([nodelist[i], nodelist[j]])
        for nodepair in nodepairs:
            task = copy.deepcopy(taskTemplate)
            task["Id"] = id
            if mode == 'Parallel'.lower():
                task["ParentIds"] = [headingNode2Id[node] for node in nodepair]
            else:
                task["ParentIds"] = [id-1]
            id += 1
            nodes = ','.join(nodepair)
            task["CommandLine"] = task["CommandLine"].replace("[dummynodes]", nodes)
            task["CommandLine"] = task["CommandLine"].replace("[pairednode]", nodepair[1])
            task["CommandLine"] = task["CommandLine"].replace("[timeout]", str(timeout))
            if debugCommand:
                task["CommandLine"] = debugCommand
            task["Node"] = nodepair[0]
            task["CustomizedData"] = '{} {}'.format(taskLabel, nodes)
            tasks.append(task)
    return tasks

def mpiPingpongGetGroups(nodelist):
    n = len(nodelist)
    if n <= 2:
        return [[[nodelist[0], nodelist[-1]]]]
    groups = []
    if n%2 == 1:
        for j in range(0, n):
            group = []
            for i in range(1, n//2+1):
                group.append([nodelist[(j+i)%n], nodelist[j-i]])
            groups.append(group)
    else:
        groups = mpiPingpongGetGroups(nodelist[1:])
        for i in range(0, len(groups)):
            groups[i].append([nodelist[0], nodelist[i+1]])
    return groups

def mpiPingpongReduce(arguments, allNodes, tasks, taskResults):
    startTime = time.time()
    nodesNumber = len(allNodes)

    # for debug
    warnings = []
    if len(tasks) != len(taskResults):
        warnings.append('Task count {} is not equal to task result count {}.'.format(len(tasks), len(taskResults)))

    defaultPacketSize = 2**22
    mpiVersion = arguments['Intel MPI version']    
    packetSize = 2**arguments['Packet size']
    mode = arguments['Mode'].lower()
    debug = arguments['Debug']

    isDefaultSize = not 2**-1 < packetSize < 2**30

    taskStateFinished = 3
    taskStateFailed = 4
    taskStateCanceled = 5

    taskId2nodePair = {}
    tasksForStatistics = set()
    windowsTaskIds = set()
    linuxTaskIds = set()
    rdmaNodes = []
    canceledTasks = []
    canceledNodePairs = set()
    hasInterVmTask = False
    try:
        for task in tasks:
            taskId = task['Id']
            state = task['State']
            taskLabel = task['CustomizedData']
            nodeOrPair = taskLabel.split()[-1]
            if '[Windows]' in taskLabel:
                windowsTaskIds.add(taskId)
            if '[Linux]' in taskLabel:
                linuxTaskIds.add(taskId)
            if '[RDMA]' in taskLabel and ',' not in taskLabel:
                rdmaNodes.append(nodeOrPair)
            taskId2nodePair[taskId] = nodeOrPair
            if ',' in nodeOrPair:
                hasInterVmTask = True
                if state == taskStateFinished:
                    tasksForStatistics.add(taskId)
            if state == taskStateCanceled:
                canceledTasks.append(taskId)
                canceledNodePairs.add(nodeOrPair)
    except Exception as e:
        printErrorAsJson('Failed to parse tasks. ' + str(e))
        return -1

    if len(windowsTaskIds) + len(linuxTaskIds) != len(tasks):
        printErrorAsJson('Lost OS type information.')
        return -1

    if not hasInterVmTask:
        printErrorAsJson('No inter VM test was executed. Please select more nodes.')
        return 0

    messages = {}
    failedTasks = []
    taskRuntime = {}
    try:
        for taskResult in taskResults:
            taskId = taskResult['TaskId']
            nodeName = taskResult['NodeName']
            nodePair = taskId2nodePair[taskId]
            exitCode = taskResult['ExitCode']
            if 'Message' in taskResult and taskResult['Message']:
                output = taskResult['Message']
                hasResult = False
                try:
                    if taskId in linuxTaskIds:
                        message = json.loads(output)
                        hasResult = message['Latency'] > 0 and message['Throughput'] > 0
                        taskRuntime[taskId] = message['Time']
                    elif exitCode == 0:
                        message = mpiPingpongParseOutput(output, isDefaultSize)
                        hasResult = True if message else False
                except:
                    pass
                if taskId in tasksForStatistics and hasResult:
                    messages[taskId2nodePair[taskId]] = message
                if exitCode != 0 or not hasResult:
                    failedTask = {
                        'TaskId':taskId,
                        'NodeName':nodeName,
                        'NodeOrPair':nodePair,
                        'ExitCode':exitCode,
                        'Output':output
                        }
                    failedTasks.append(failedTask)
            else:
                raise Exception('No Message')
    except Exception as e:
        printErrorAsJson('Failed to parse task result. Task id: {}. {}'.format(taskId, e))
        return -1

    latencyThreshold = packetSize//50 if packetSize > 2**20 else 10000
    throughputThreshold = packetSize//1000 if 2**-1 < packetSize < 2**20 else 50
    if len(rdmaNodes) == len(allNodes):
        latencyThreshold = 2**3 if packetSize < 2**13 else packetSize/2**10
        throughputThreshold = packetSize/2**3 if 2**-1 < packetSize < 2**13 else 2**10
    if mode == 'Parallel'.lower():
        latencyThreshold = 1000000
        throughputThreshold = 0

    goodPairs = [pair for pair in messages if messages[pair]['Throughput'] > throughputThreshold]
    goodNodesGroups = mpiPingpongGetGroupsOfFullConnectedNodes(goodPairs)
    goodNodes = set([node for group in goodNodesGroups for node in group])
    if goodNodes != set([node for pair in goodPairs for node in pair.split(',')]):
        printErrorAsJson('Should not get here!')
        return -1
    if nodesNumber == 1 or nodesNumber == 2 and len(rdmaNodes) == 1:
        goodNodes = [task['Node'] for task in tasks if task['State'] == taskStateFinished]
    badNodes = [node for node in allNodes if node not in goodNodes]
    goodNodes = list(goodNodes)
    failedReasons, failedReasonsByNode = mpiPingpongGetFailedReasons(failedTasks, mpiVersion, canceledNodePairs)

    result = {
        'GoodNodesGroups':mpiPingpongGetLargestNonoverlappingGroups(goodNodesGroups),
        'GoodNodes':goodNodes,
        'FailedNodes':failedReasonsByNode,
        'BadNodes':badNodes,
        'RdmaNodes':rdmaNodes,
        'FailedReasons':failedReasons,
        'Latency':{},
        'Throughput':{},
        }

    if messages:
        nodesInMessages = [node for nodepair in messages.keys() for node in nodepair.split(',')]
        nodesInMessages = list(set(nodesInMessages))
        messagesByNode = {}
        for pair in messages:
            for node in pair.split(','):
                messagesByNode.setdefault(node, {})[pair] = messages[pair]
        histogramSize = 8

        statisticsItems = ['Latency', 'Throughput']
        for item in statisticsItems:
            data = [messages[pair][item] for pair in messages]
            globalMin = numpy.amin(data)
            globalMax = numpy.amax(data)
            factor = math.ceil(globalMax / histogramSize)
            histogramBins = [factor * n for n in range(histogramSize + 1)]
            histogram = [list(array) for array in numpy.histogram(data, bins=histogramBins)]

            if item == 'Latency':
                unit = 'us'
                threshold = latencyThreshold
                badPairs = [{'Pair':pair, 'Value':messages[pair][item]} for pair in messages if messages[pair][item] > latencyThreshold]
                badPairs.sort(key=lambda x:x['Value'], reverse=True)
                bestPairs = {'Pairs':[pair for pair in messages if messages[pair][item] == globalMin], 'Value':globalMin}
                worstPairs = {'Pairs':[pair for pair in messages if messages[pair][item] == globalMax], 'Value':globalMax}
                packet_size = 0 if packetSize == 2**-1 else packetSize
            else:
                unit = 'MB/s'
                threshold = throughputThreshold
                badPairs = [{'Pair':pair, 'Value':messages[pair][item]} for pair in messages if messages[pair][item] < throughputThreshold]
                badPairs.sort(key=lambda x:x['Value'])
                bestPairs = {'Pairs':[pair for pair in messages if messages[pair][item] == globalMax], 'Value':globalMax}
                worstPairs = {'Pairs':[pair for pair in messages if messages[pair][item] == globalMin], 'Value':globalMin}
                packet_size = defaultPacketSize if packetSize == 2**-1 else packetSize

            result[item]['Unit'] = unit
            result[item]['Threshold'] = threshold
            result[item]['Packet_size'] = str(packet_size) + ' Bytes'
            result[item]['Result'] = {}
            result[item]['Result']['Passed'] = len(badPairs) == 0
            result[item]['Result']['Bad_pairs'] = badPairs
            result[item]['Result']['Best_pairs'] = bestPairs
            result[item]['Result']['Worst_pairs'] = worstPairs
            result[item]['Result']['Histogram'] = mpiPingpongRenderHistogram(histogram)
            result[item]['Result']['Average'] = numpy.average(data)
            result[item]['Result']['Median'] = numpy.median(data)
            result[item]['Result']['Standard_deviation'] = numpy.std(data)
            result[item]['Result']['Variability'] = mpiPingpongGetVariability(data)
            
            result[item]['ResultByNode'] = {}
            for node in nodesInMessages:
                data = [messagesByNode[node][pair][item] for pair in messagesByNode[node]]
                histogram = [list(array) for array in numpy.histogram(data, bins=histogramBins)]
                if item == 'Latency':
                    badPairs = [{'Pair':pair, 'Value':messagesByNode[node][pair][item]} for pair in messagesByNode[node] if messagesByNode[node][pair][item] > latencyThreshold and node in pair.split(',')]
                    badPairs.sort(key=lambda x:x['Value'], reverse=True)
                    bestPairs = {'Pairs':[pair for pair in messagesByNode[node] if messagesByNode[node][pair][item] == numpy.amin(data) and node in pair.split(',')], 'Value':numpy.amin(data)}
                    worstPairs = {'Pairs':[pair for pair in messagesByNode[node] if messagesByNode[node][pair][item] == numpy.amax(data) and node in pair.split(',')], 'Value':numpy.amax(data)}
                else:
                    badPairs = [{'Pair':pair, 'Value':messagesByNode[node][pair][item]} for pair in messagesByNode[node] if messagesByNode[node][pair][item] < throughputThreshold and node in pair.split(',')]
                    badPairs.sort(key=lambda x:x['Value'])
                    bestPairs = {'Pairs':[pair for pair in messagesByNode[node] if messagesByNode[node][pair][item] == numpy.amax(data) and node in pair.split(',')], 'Value':numpy.amax(data)}
                    worstPairs = {'Pairs':[pair for pair in messagesByNode[node] if messagesByNode[node][pair][item] == numpy.amin(data) and node in pair.split(',')], 'Value':numpy.amin(data)}
                result[item]['ResultByNode'][node] = {}
                result[item]['ResultByNode'][node]['Bad_pairs'] = badPairs
                result[item]['ResultByNode'][node]['Passed'] = len(badPairs) == 0
                result[item]['ResultByNode'][node]['Best_pairs'] = bestPairs
                result[item]['ResultByNode'][node]['Worst_pairs'] = worstPairs
                result[item]['ResultByNode'][node]['Histogram'] = mpiPingpongRenderHistogram(histogram)
                result[item]['ResultByNode'][node]['Average'] = numpy.average(data)
                result[item]['ResultByNode'][node]['Median'] = numpy.median(data)
                result[item]['ResultByNode'][node]['Standard_deviation'] = numpy.std(data)
                result[item]['ResultByNode'][node]['Variability'] = mpiPingpongGetVariability(data)

    endTime = time.time()
    
    if debug:
        taskRuntime = {
            'Max': numpy.amax(list(taskRuntime.values())),
            'Ave': numpy.average(list(taskRuntime.values())),
            'Sorted': sorted([{'runtime':taskRuntime[key], 'taskId':key, 'nodepair':taskId2nodePair[key]} for key in taskRuntime], key=lambda x:x['runtime'], reverse=True)
            }
        failedTasksByExitcode = {}
        for task in failedTasks:
            failedTasksByExitcode.setdefault(task['ExitCode'], []).append(task['TaskId'])
        result['DebugInfo'] = {
            'ReduceRuntime':endTime - startTime,
            'GoodNodesGroups':goodNodesGroups,
            'CanceledTasks':canceledTasks,
            'FailedTasksGroupByExitcode':failedTasksByExitcode,
            'Warnings':warnings,
            'TaskRuntime':taskRuntime,
            }
        
    print(json.dumps(result))
    return 0

def mpiPingpongParseOutput(output, isDefaultSize):
    lines = output.splitlines()
    title = '#bytes #repetitions      t[usec]   Mbytes/sec'
    hasResult = False
    data = []
    for line in lines:
        if hasResult:
            numbers = line.split()
            if len(numbers) == 4:
                data.append(numbers)
            else:
                break
        elif title in line:
            hasResult = True
    if isDefaultSize and len(data) == 24:
        return {
            'Latency': float(data[0][2]),
            'Throughput': float(data[-1][3])
        }
    if not isDefaultSize and len(data) == 3:
        return {
            'Latency': float(data[1][2]),
            'Throughput': float(data[1][3])
        }

def mpiPingpongGetFailedReasons(failedTasks, mpiVersion, canceledNodePairs):
    reasonMpiNotInstalled = 'Intel MPI is not found.'
    solutionMpiNotInstalled = 'Please ensure Intel MPI {} is installed on the default location. Run diagnostics test "Prerequisite-Intel MPI Installation" on the nodes if it is not installed on them.'.format(mpiVersion)

    reasonHostNotFound = 'The node pair may be not in the same network or there is issue when parsing host name.'
    solutionHostNotFound = 'Check DNS server and ensure the node pair could translate the host name to address of each other.'

    reasonFireWall = 'The connection was blocked by firewall.'
    reasonFireWallProbably = 'The connection may be blocked by firewall.'
    solutionFireWall = 'Check and configure the firewall properly.'

    reasonNodeSingleCore = 'MPI PingPong can not run inside a node with only 1 core.'
    solutionNodeSingleCore = 'Ignore this failure.'

    reasonTaskTimeout = 'Task timeout.'
    reasonPingpongTimeout = 'Pingpong test timeout.'
    reasonSampleTimeout = 'Pingpong test sample timeout.'
    reasonNoResult = 'No result.'

    reasonWgetFailed = 'Failed to download filter script.'
    solutionWgetFailed = 'Check accessibility of "$blobEndpoint/diagtestscripts/mpi-pingpong-filter.py" on nodes.'

    reasonAvSet = 'The nodes may not be in the same availability set.(CM ADDR ERROR)'
    solutionAvSet = 'Recreate the node(s) and ensure the nodes are in the same availability set.'
    
    reasonDapl = 'MPI issue: "dapl fabric is not available and fallback fabric is not enabled"'
    solutionDapl = 'Please re-create the VM.'

    failedReasons = {}
    for failedPair in failedTasks:
        reason = "Unknown"
        nodeName = failedPair['NodeName']
        nodeOrPair = failedPair['NodeOrPair']
        output = failedPair['Output']
        exitCode = failedPair['ExitCode']
        pairedNode = nodeOrPair.split(',')[-1]
        if "mpivars.sh: No such file or directory" in output or 'The system cannot find the path specified' in output:
            reason = reasonMpiNotInstalled
            failedNode = nodeName
            failedPair['NodeOrPair'] = failedNode
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionMpiNotInstalled, 'Nodes':set()})['Nodes'].add(failedNode)
        elif "linux/mpi/intel64/bin/pmi_proxy: No such file or directory" in output or 'pmi_proxy not found on {}. Set Intel MPI environment variables'.format(pairedNode) in output:
            reason = reasonMpiNotInstalled
            failedNode = pairedNode
            failedPair['NodeOrPair'] = failedNode
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionMpiNotInstalled, 'Nodes':set()})['Nodes'].add(failedNode)            
        elif "Host {} not found:".format(pairedNode) in output:
            reason = reasonHostNotFound
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionHostNotFound, 'NodePairs':[]})['NodePairs'].append(nodeOrPair)
        elif "check for firewalls!" in output:
            reason = reasonFireWall
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionFireWall, 'NodePairs':[]})['NodePairs'].append(nodeOrPair)
        elif "Assertion failed in file ../../src/mpid/ch3/channels/nemesis/netmod/tcp/socksm.c at line 2988: (it_plfd->revents & POLLERR) == 0" in output:
            reason = reasonFireWallProbably
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionFireWall, 'NodePairs':[]})['NodePairs'].append(nodeOrPair)
        elif "Benchmark PingPong invalid for 1 processes" in output:
            reason = reasonNodeSingleCore
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionNodeSingleCore, 'Nodes':[]})['Nodes'].append(nodeName)
        elif "wget" in output and exitCode == 4 or 'mpi-pingpong-filter.py' in output and exitCode == 8:
            reason = reasonWgetFailed
            failedPair['NodeOrPair'] = nodeName
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionWgetFailed, 'Nodes':set()})['Nodes'].add(nodeName)
        elif "CM ADDR ERROR" in output:
            reason = reasonAvSet
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionAvSet, 'NodePairs':[]})['NodePairs'].append(nodeOrPair)
        elif "dapl fabric is not available and fallback fabric is not enabled" in output:
            reason = reasonDapl
            failedNode = nodeName
            if '[1] MPI startup(): dapl fabric is not available and fallback fabric is not enabled' in output:
                failedNode = pairedNode
            failedPair['NodeOrPair'] = failedNode
            failedReasons.setdefault(reason, {'Reason':reason, 'Solution':solutionDapl, 'Nodes':set()})['Nodes'].add(failedNode)            
        else:
            if "Time limit (secs_per_sample * msg_sizes_list_len) is over;" in output:
                reason = reasonSampleTimeout
            elif exitCode == 124:
                reason = reasonPingpongTimeout
            elif nodeOrPair in canceledNodePairs:
                reason = reasonTaskTimeout
            elif output.split('\n', 1)[0] == '[Message before filter]:':
                reason = reasonNoResult
            failedReasons.setdefault(reason, {'Reason':reason, 'NodePairs':[]})['NodePairs'].append(nodeOrPair)
        failedPair['Reason'] = reason
    if reasonMpiNotInstalled in failedReasons:
        failedReasons[reasonMpiNotInstalled]['Nodes'] = list(failedReasons[reasonMpiNotInstalled]['Nodes'])
    if reasonWgetFailed in failedReasons:
        failedReasons[reasonWgetFailed]['Nodes'] = list(failedReasons[reasonWgetFailed]['Nodes'])
    if reasonDapl in failedReasons:
        failedReasons[reasonDapl]['Nodes'] = list(failedReasons[reasonDapl]['Nodes'])

    failedReasonsByNode = {}
    for failedTask in failedTasks:
        nodeOrPair = failedTask['NodeOrPair']
        for node in nodeOrPair.split(','):
            failedReasonsByNode.setdefault(node, {}).setdefault(failedTask['Reason'], []).append(nodeOrPair)
            severity = failedReasonsByNode[node].setdefault('Severity', 0)
            failedReasonsByNode[node]['Severity'] = severity + 1
    for value in failedReasonsByNode.values():
        nodesOrPairs = value.get(reasonMpiNotInstalled)
        if nodesOrPairs:
            value[reasonMpiNotInstalled] = list(set(nodesOrPairs))
    for key in failedReasonsByNode.keys():
        severity = failedReasonsByNode[key].pop('Severity')
        failedReasonsByNode["{} ({})".format(key, severity)] = failedReasonsByNode.pop(key)

    return (list(failedReasons.values()), failedReasonsByNode)

def mpiPingpongGetNodeMap(pairs):
    connectedNodesOfNode = {}
    for pair in pairs:
        nodes = pair.split(',')
        connectedNodesOfNode.setdefault(nodes[0], set()).add(nodes[1])
        connectedNodesOfNode.setdefault(nodes[1], set()).add(nodes[0])
    return connectedNodesOfNode

def mpiPingpongGetLargestNonoverlappingGroups(groups):
    largestGroups = []
    visitedNodes = set()
    while len(groups):
        maxLen = max([len(group) for group in groups])
        largestGroup = [group for group in groups if len(group) == maxLen][0]
        largestGroups.append(largestGroup)
        visitedNodes.update(largestGroup)
        groupsToRemove = []
        for group in groups:
            for node in group:
                if node in visitedNodes:
                    groupsToRemove.append(group)
                    break
        groups = [group for group in groups if group not in groupsToRemove]
    return largestGroups

def mpiPingpongGetGroupsOfFullConnectedNodes(pairs):
    connectedNodesOfNode = mpiPingpongGetNodeMap(pairs)
    nodes = list(connectedNodesOfNode.keys())
    if not nodes:
        return []
    groups = [set([nodes[0]])]
    for node in nodes[1:]:
        newGroups = []
        for group in groups:
            newGroup = group & connectedNodesOfNode[node]
            newGroup.add(node)
            mpiPingpongAddToGroups(newGroups, newGroup)
        for group in newGroups:
            mpiPingpongAddToGroups(groups, group)
    return [list(group) for group in groups]

def mpiPingpongAddToGroups(groups, new):
    for old in groups:
        if old <= new or old >= new:
            old |= new
            return
    groups.append(new)

def mpiPingpongRenderHistogram(histogram):
    values = [int(value) for value in histogram[0]]
    binEdges = histogram[1]
    return [values, ["{0:.2f}".format(binEdges[i-1]) + '-' + "{0:.2f}".format(binEdges[i]) for i in range(1, len(binEdges))]]

def mpiPingpongGetVariability(data):
    variability = numpy.std(data)/max(numpy.average(data), 10**-6)
    if variability < 0.05:
        return "Low"
    elif variability < 0.25:
        return "Moderate"
    else:
        return "High"

def mpiRingMap(arguments, windowsNodes, linuxNodes, rdmaNodes):
    mpiVersion = arguments['Intel MPI version']
    globalCheckIntelProductVersion('MPI', mpiVersion)
    mpiInstallationLocationWindows = globalGetDefaultInstallationLocationWindows('MPI', mpiVersion)
    mpiInstallationLocationLinux = globalGetDefaultInstallationLocationLinux('MPI', mpiVersion)

    if windowsNodes and linuxNodes:
        raise Exception('Can not run this test among Linux nodes and Windows nodes')

    nodelist = list(windowsNodes) if windowsNodes else list(linuxNodes)
    if 0 < len(rdmaNodes) < len(nodelist):
        raise Exception('Can not run this test among RDMA nodes and non-RDMA nodes')
    
    taskLabel = '{}{}'.format('[Windows]' if windowsNodes else '[Linux]', '[RDMA]' if rdmaNodes else '')
    rdmaOption = '-env I_MPI_FABRICS=shm:dapl -env I_MPI_DAPL_PROVIDER=ofa-v2-ib0' if rdmaNodes else ''
    nodes = ','.join(nodelist)
    nodesCount = len(nodelist)

    taskTemplateWindows = {
        'UserName': HPC_DIAG_USERNAME,
        'Password': HPC_DIAG_PASSWORD,
        'EnvironmentVariables': {'CCP_ISADMIN': 1}
    }

    taskTemplateLinux = {
        'UserName':HPC_DIAG_USERNAME,
        'Password':None,
        'PrivateKey':SSH_PRIVATE_KEY,
    }

    taskTemplate = taskTemplateWindows if windowsNodes else taskTemplateLinux

    mpiEnvFile = r'{}\intel64\bin\mpivars.bat'.format(mpiInstallationLocationWindows)
    commandSetFirewall = r'netsh firewall add allowedprogram "{}\intel64\bin\mpiexec.exe" hpc_diagnostics_mpi'.format(mpiInstallationLocationWindows)
    commandRunIntra = r'\\"%USERDOMAIN%\%USERNAME%`n{}\\" | mpiexec {} IMB-MPI1 sendrecv'.format(HPC_DIAG_PASSWORD, rdmaOption)
    commandRunInter = r'\\"%USERDOMAIN%\%USERNAME%`n{}\\" | mpiexec {} -hosts {} -ppn 1 IMB-MPI1 -npmin {} sendrecv'.format(HPC_DIAG_PASSWORD, rdmaOption, nodes, nodesCount)
    commandMeasureTime = "$stopwatch = [system.diagnostics.stopwatch]::StartNew(); [command]; if($?) {'Run time: ' + $stopwatch.Elapsed.TotalSeconds}"
    commandRunWindows = '{} && "{}" && powershell "{}"'.format(commandSetFirewall, mpiEnvFile, commandMeasureTime)
    commandRunIntraWindows = commandRunWindows.replace('[command]', commandRunIntra)
    commandRunInterWindows = commandRunWindows.replace('[command]', commandRunInter)

    commandSource = 'source {0}/intel64/bin/mpivars.sh'.format(mpiInstallationLocationLinux)
    commandRunIntraLinux = '{} && time mpirun -env I_MPI_SHM_LMT=shm {} IMB-MPI1 sendrecv'.format(commandSource, rdmaOption)
    commandRunInterLinux = '{} && time mpirun -hosts {} {} -ppn 1 IMB-MPI1 -npmin {} sendrecv'.format(commandSource, nodes, rdmaOption, nodesCount)

    taskId = 1
    tasks = []
    for node in nodelist:
        task = copy.deepcopy(taskTemplate)
        task['Id'] = taskId
        taskId += 1
        task['Node'] = node
        task['CommandLine'] = commandRunIntraWindows if windowsNodes else commandRunIntraLinux
        task['CustomizedData'] = '{} {}'.format(taskLabel, node)
        task['MaximumRuntimeSeconds'] = 60
        tasks.append(task)

    if nodesCount > 1:
        task = copy.deepcopy(taskTemplate)
        task['Id'] = taskId
        taskId += 1
        task['Node'] = nodelist[0]
        task['ParentIds'] = list(range(1, nodesCount + 1))
        task['CommandLine'] = commandRunInterWindows if windowsNodes else commandRunInterLinux
        task['CustomizedData'] = '{} {}'.format(taskLabel, nodes)
        if linuxNodes:
            task['EnvironmentVariables'] = {'CCP_NODES': '{} {}'.format(nodesCount, ' '.join(['{} 1'.format(node) for node in nodelist]))}
        task['MaximumRuntimeSeconds'] = 120
        tasks.append(task)
    
    print(json.dumps(tasks))

def mpiRingReduce(nodes, tasks, taskResults):
    output = None
    try:
        for taskResult in taskResults:
            taskId = taskResult['TaskId']
            if taskId == 1 and len(nodes) == 1 or taskId == len(nodes) + 1:
                if taskResult['ExitCode'] == 0:
                    output = taskResult['Message']
                    break
    except Exception as e:
        printErrorAsJson('Failed to parse task result. ' + str(e))
        return -1
    
    rows = []
    if output:
        data = output.splitlines()
        title = '#bytes #repetitions  t_min[usec]  t_max[usec]  t_avg[usec]   Mbytes/sec'
        hasResult = False
        for line in data:
            if hasResult:
                row = line.split()
                if len(row) != len(title.split()):
                    break
                rows.append({
                    'Message_Size':{
                        'value':row[0],
                        'unit':'Bytes'
                    },
                    'Latency':{
                        'value':row[-2],
                        'unit':'usec'
                    },
                    'Throughput':{
                        'value':row[-1],
                        'unit':'Mbytes/sec'
                    }
                })
            elif title in line:
                hasResult = True
    
    result = {
        'Description': 'This data shows the {} communication performance as latencies and throughputs for various MPI message sizes, which are extracted from the result of running Intel MPI-1 Benchmark Sendrecv, more refer to https://software.intel.com/en-us/imb-user-guide-sendrecv'.format('intra-VM' if len(nodes) == 1 else 'inter-VM'),
        'Result': rows
        }
    
    print(json.dumps(result))
    return 0

def installIntelProductMap(arguments, windowsNodes, linuxNodes, product):
    version = arguments['Version'].lower()
    timeout = arguments['Max runtime']
    globalCheckIntelProductVersion(product, version)

    leastTime = 180 if product == 'MPI' else 600
    timeout -= leastTime - 1
    if timeout <= 0:
        raise Exception('The Max runtime parameter should be equal or larger than {}'.format(leastTime))
            
    # command to install MPI/MKL on Linux node
    uri = INTEL_PRODUCT_URI[product][version]['Linux']
    installDirectory = globalGetDefaultInstallationLocationLinux(product, version)
    wgetOutput = 'wget.output'
    commandCheckExist = "[ -d {0} ] && echo 'Already installed in {0}'".format(installDirectory)
    commandShowOutput = r"cat {} | sed 's/.*\r//'".format(wgetOutput)
    commandDownload = 'timeout {0}s wget --progress=bar:force -O intel.tgz {1} 1>{2} 2>&1 && {3} || (errorcode=$? && {3} && exit $errorcode)'.format(timeout, uri, wgetOutput, commandShowOutput)
    commandInstall = "tar -zxf intel.tgz && cd l_mpi_* && sed -i -e 's/ACCEPT_EULA=decline/ACCEPT_EULA=accept/g' ./silent.cfg && ./install.sh --silent ./silent.cfg"
    commandLinux = '{} || ({} && {})'.format(commandCheckExist, commandDownload, commandInstall)

    # command to install MPI/MKL on Windows node
    uri = INTEL_PRODUCT_URI[product][version]['Windows']
    installDirectory = globalGetDefaultInstallationLocationWindows(product, version)
    commandWindows = """powershell "
if (Test-Path '[installDirectory]')
{
    'Already installed in [installDirectory]';
    exit
}
else
{
    date;
    $stopwatch = [system.diagnostics.stopwatch]::StartNew();
    'Start downloading';
    $client = new-object System.Net.WebClient;
    $client.DownloadFile('[uri]', '[product].exe');
    date;
    'End downloading';
    if ($stopwatch.Elapsed.TotalSeconds -gt [timeout])
    {
        'Not enough time to install before task timeout. Exit.';
        exit 124;
    }
    else
    {
        cmd /C '.\[product].exe --silent --a install --eula=accept --output=%cd%\[product].log & type [product].log'
    }
}"
""".replace('[installDirectory]', installDirectory).replace('[uri]', uri).replace('[timeout]', str(timeout)).replace('[product]', product).replace('\n', '')

    tasks = []
    id = 1
    for node in windowsNodes:
        task = {}
        task["Id"] = id
        id += 1
        task["Node"] = node
        task["CommandLine"] = commandWindows
        task["CustomizedData"] = 'Windows'
        task["MaximumRuntimeSeconds"] = 36000
        tasks.append(task)
    for node in linuxNodes:
        task = {}
        task["Id"] = id
        id += 1
        task["Node"] = node
        task["CommandLine"] = commandLinux
        task["CustomizedData"] = 'Linux'
        task["MaximumRuntimeSeconds"] = 36000
        tasks.append(task)

    print(json.dumps(tasks))

def installIntelProductReduce(arguments, tasks, taskResults, product):
    version = arguments['Version']

    taskStateCanceled = 5
    canceledTasks = set()
    osTypeByNode = {}
    try:
        for task in tasks:
            osTypeByNode[task['Node']] = task['CustomizedData']
            if task['State'] == taskStateCanceled:
                canceledTasks.add(task['Id'])
    except Exception as e:
        printErrorAsJson('Failed to parse tasks. ' + str(e))
        return -1

    results = {}
    try:
        for taskResult in taskResults:
            node = taskResult['NodeName']
            message = taskResult['Message']
            result = 'Installation Failed'
            if taskResult['ExitCode'] == 0:
                if 'Already installed' in message.split('\n', 1)[0]:
                    result = 'Already installed'
                elif osTypeByNode[node].lower() == 'Linux'.lower() or 'installation was completed successfully' in message:
                    result = 'Installation succeeded'
            elif taskResult['ExitCode'] == 124 or taskResult['TaskId'] in canceledTasks:
                result = 'Timeout'
            results[node] = result
    except Exception as e:
        printErrorAsJson('Failed to parse task result. ' + str(e))
        return -1

    htmlRows = []
    for node in sorted(results):
        htmlRows.append(
            '\n'.join([
                '  <tr>',
                '\n'.join(['    <td>{}</td>'.format(column) for column in [node, osTypeByNode[node], results[node]]]),
                '  </tr>'
                ])) 

    description = 'This is the result of installing Intel {} {} on each node.'.format(product, version)
    mpiLink = '<a target="_blank" rel="noopener noreferrer" href="https://software.intel.com/en-us/mpi-library">Intel MPI</a>'
    mklLink = '<a target="_blank" rel="noopener noreferrer" href="https://software.intel.com/en-us/mkl">Intel MKL</a>'
    html = '''
<!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
</style>
</head>
<body>
<h2>Intel MPI Installation</h2>
<table>
  <tr>
    <th>Node</th>
    <th>OS</th>
    <th>Result</th>
  </tr>
''' + '\n'.join(htmlRows) + '''
</table>
<p>''' + description.replace('Intel MPI', mpiLink).replace('Intel MKL', mklLink) + '''</p>
</body>
</html>
'''

    result = {
        'Description': description,
        'Results': results,
        'Html': html
        }

    print(json.dumps(result))
    return 0

def benchmarkLinpackMap(arguments, windowsNodes, linuxNodes, vmSizeByNode):
    intelMklVersion = arguments['Intel MKL version'].lower()
    sizeLevel = arguments['Size level']
    globalCheckIntelProductVersion('MKL', intelMklVersion)
    intelMklLocation = globalGetDefaultInstallationLocationLinux('MKL', intelMklVersion)
    if not 1 <= sizeLevel <= 15:
        raise Exception('Parameter "Size level" should be in range 1 - 15')

    commandInstallNumactlOnUbuntu = 'apt install -y numactl'
    commandInstallNumactlOnSuse = 'zypper install -y numactl'
    commandInstallNumactlOnOthers = 'yum install -y numactl'
    commandInstallNumactlQuietOrWarn = "({}) >/dev/null 2>&1 || echo 'Failed to install numactl.'"
    commandInstallNumactlOnUbuntu = commandInstallNumactlQuietOrWarn.format(commandInstallNumactlOnUbuntu)
    commandInstallNumactlOnSuse = commandInstallNumactlQuietOrWarn.format(commandInstallNumactlOnSuse)
    commandInstallNumactlOnOthers = commandInstallNumactlQuietOrWarn.format(commandInstallNumactlOnOthers)
    commandDetectDistroAndInstall = ("cat /etc/*release > distroInfo && "
                                 "if cat distroInfo | grep -Fiq 'Ubuntu'; then {};"
                                 "elif cat distroInfo | grep -Fiq 'Suse'; then {};"
                                 "elif cat distroInfo | grep -Fiq 'CentOS'; then {};"
                                 "elif cat distroInfo | grep -Fiq 'Redhat'; then {};"
                                 "elif cat distroInfo | grep -Fiq 'Red Hat'; then {};"
                                 "fi").format(commandInstallNumactlOnUbuntu, 
                                              commandInstallNumactlOnSuse,
                                              commandInstallNumactlOnOthers,
                                              commandInstallNumactlOnOthers,
                                              commandInstallNumactlOnOthers)

    commandModify = "sed -i 's/.*# number of tests/{} # number of tests/' lininput_xeon64".format(sizeLevel)
    commandRunLinpack = 'cd {}/benchmarks/linpack && {} && ./runme_xeon64'.format(intelMklLocation, commandModify)
    commandCheckCpu = "lscpu | egrep '^CPU\(s\)|Model name'"

    # Bug: the output of task is empty when it runs Linpack with large problem size, thus start another task to collect the output
    tempOutputDir = '/tmp/hpc_diag_linpack_standalone'
    commandCreateTempOutputDir = 'mkdir -p {}'.format(tempOutputDir)

    tasks = []
    id = 1
    for node in linuxNodes:
        outputFile = '{}/{}'.format(tempOutputDir, uuid.uuid4())
        commandClearFile = 'rm -f {}'.format(outputFile)
        task = {}
        task['Id'] = id
        task['Node'] = node
        task['CustomizedData'] = '[Linux] {}'.format(vmSizeByNode[node])
        task['CommandLine'] = '{} && {} && ({} && {}) 2>&1 | tee {}'.format(commandClearFile, commandCreateTempOutputDir, commandDetectDistroAndInstall, commandRunLinpack, outputFile)
        task['MaximumRuntimeSeconds'] = 36000
        tasks.append(task)
        task = copy.deepcopy(task)
        task['ParentIds'] = [id]
        task['Id'] += 1
        task['CommandLine'] = '{}; cat {} && {}'.format(commandCheckCpu, outputFile, commandClearFile)
        tasks.append(task)
        id += 2

    for node in windowsNodes:
        task = {}
        task['Id'] = id
        id += 1
        task['Node'] = node
        task['CustomizedData'] = '[Windows] {}'.format(vmSizeByNode[node])
        task['CommandLine'] = 'echo This test is not supported yet on Windows node'
        tasks.append(task)

    print(json.dumps(tasks))

def benchmarkLinpackReduce(arguments, tasks, taskResults):
    intelMklVersion = arguments['Intel MKL version'].lower()
    intelMklLocation = globalGetDefaultInstallationLocationLinux('MKL', intelMklVersion)
        
    windowsNodes = set()
    linuxNodes = set()
    taskDetail = {}
    try:
        for task in tasks:
            taskId = task['Id']
            node = task['Node']
            tasklabel = task['CustomizedData']
            if tasklabel.startswith('[Windows]'):
                windowsNodes.add(node)
            if tasklabel.startswith('[Linux]'):
                linuxNodes.add(node)
            if node in linuxNodes and taskId % 2 == 0 or node in windowsNodes:
                size = tasklabel
                taskDetail[taskId] = {
                    'Node': node,
                    'Size': size,
                    'Output': None
                    }
    except Exception as e:
        printErrorAsJson('Failed to parse tasks. ' + str(e))
        return -1

    nodesWithoutIntelMklInstalled = []
    nodesFailedToInstallNumactl = []
    try:
        for taskResult in taskResults:
            taskId = taskResult['TaskId']
            nodeName = taskResult['NodeName']
            output = taskResult['Message']
            if nodeName in linuxNodes and taskId % 2 == 0:
                taskDetail[taskId]['Output'] = output
                if 'Failed to install numactl' in output:
                    nodesFailedToInstallNumactl.append(nodeName)
                if 'benchmarks/linpack: No such file or directory' in output:
                    nodesWithoutIntelMklInstalled.append(nodeName)
    except Exception as e:
        printErrorAsJson('Failed to parse task results. ' + str(e))
        return -1

    defaultFlopsPerCycle = 16 # Use this default value because currently it seems that the Intel microarchitectures used in Azure VM are in "Intel Haswell/Broadwell/Skylake/Kaby Lake". Consider getting this value from test parameter in case new Azure VM sizes are introduced.

    results = list(taskDetail.values())
    htmlRows = []
    for task in results:
        perf, N, coreCount, coreFreq = benchmarkLinpackParseTaskOutput(task['Output'])
        theoreticalPerfExpr = "{} * {} * {}".format(coreCount, defaultFlopsPerCycle, coreFreq) if coreCount and coreFreq else None
        theoreticalPerf = eval(theoreticalPerfExpr) if theoreticalPerfExpr else None
        efficiency = perf / theoreticalPerf if perf and theoreticalPerf else None
        task['TheoreticalPerf'] = theoreticalPerf
        task['Perf'] = perf
        task['N'] = N
        task['Efficiency'] = efficiency
        theoreticalPerfInHtml = "{} = {}".format(theoreticalPerfExpr, theoreticalPerf) if theoreticalPerfExpr else None
        perfInHtml = "{:.1f}".format(perf) if perf else None
        efficiencyInHtml = "{:.1%}".format(efficiency) if efficiency else None
        htmlRows.append(
            '\n'.join([
                '  <tr>',
                '\n'.join(['    <td>{}</td>'.format(item) for item in [task['Node'], task['Size'], theoreticalPerfInHtml, perfInHtml, N, efficiencyInHtml]]),
                '  </tr>'
                ]))
        del task['Output']

    intelLinpack = 'Intel Optimized LINPACK Benchmark'
    description = 'This is the result of running {} on each node.'.format(intelLinpack)
    intelLinpackLink = '<a target="_blank" rel="noopener noreferrer" href="https://software.intel.com/en-us/mkl-linux-developer-guide-intel-optimized-linpack-benchmark-for-linux">{}</a>'.format(intelLinpack)
    theoreticalPerfDescription = "The theoretical peak performance of each node is calculated by: [core count of node] * [(double-precision) floating-point operations per cycle] * [average frequency of core]" if any([task['TheoreticalPerf'] for task in results]) else ''
    intelMklNotFound = 'Intel MKL {} is not found in <b>{}</b> on node(s): {}'.format(intelMklVersion, intelMklLocation, ', '.join(nodesWithoutIntelMklInstalled)) if nodesWithoutIntelMklInstalled else ''
    installIntelMkl = 'Diagnostics test <b>Prerequisite-Intel MKL Installation</b> can be used to install Intel MKL.' if nodesWithoutIntelMklInstalled else ''
    installNumactl = 'Please install <b>numactl</b> manually, if necessary, on node(s): {}'.format(', '.join(nodesFailedToInstallNumactl)) if nodesFailedToInstallNumactl else ''
    windowsNotSupport = 'The test is not supported on Windows node currently.' if windowsNodes else ''
    html = '''
<!DOCTYPE html>
<html>
<head>
<style>
table {
    font-family: arial, sans-serif;
    border-collapse: collapse;
    width: 100%;
}
td, th {
    border: 1px solid #dddddd;
    text-align: left;
    padding: 8px;
}
</style>
</head>
<body>
<h2>Linpack standalone benchmark</h2>
<table>
  <tr>
    <th>Node</th>
    <th>OS/Node size</th>
    <th>Theoretical peak performance(GFlop/s)</th>
    <th>Best performance(GFlop/s)</th>
    <th>Problem size</th>
    <th>Efficiency</th>
  </tr>
''' + '\n'.join(htmlRows) + '''
</table>
<p>''' + description.replace(intelLinpack, intelLinpackLink) + '''</p>
<p>''' + theoreticalPerfDescription + '''</p>
<p>''' + intelMklNotFound + '''</p>
<p>''' + installIntelMkl + '''</p>
<p>''' + installNumactl + '''</p>
<p>''' + windowsNotSupport + '''</p>
</body>
</html>
'''

    result = {
        'Description': description,
        'Results': results,
        'Html': html
        }

    print(json.dumps(result, indent = 4))
    return 0

def benchmarkLinpackParseTaskOutput(raw):
    bestPerf = n = coreCount = coreFreq = None
    try:
        start = raw.find('Performance Summary (GFlops)')
        end = raw.find('Residual checks PASSED')
        if -1 < start < end:
            table = [line for line in raw[start:end].splitlines() if line.strip()][2:]
            bestPerf = 0
            for line in table:
                numbers = line.split()
                perf = float(numbers[3])
                if perf > bestPerf:
                    bestPerf = perf
                    n = int(numbers[0])
        cpuInfo = raw.split('\n', 2)[:2]
        if len(cpuInfo) == 2:
            firstLine = cpuInfo[0]
            secondLine = cpuInfo[1]
            if firstLine.startswith('CPU') and secondLine.startswith('Model name'):
                coreCount = int(firstLine.split()[-1])
                coreFreq = float([word for word in secondLine.split() if word.endswith('GHz')][0][:-3])
    except:
        pass
    return (bestPerf, n, coreCount, coreFreq)

def printErrorAsJson(errormessage):
    print(json.dumps({"Error":errormessage}))

if __name__ == '__main__':
    main()
