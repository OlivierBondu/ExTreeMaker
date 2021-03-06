#Where is the condor FARM
farmPATH = "/nfs/user/acaudron/ControlPlots/cp5314p1/FARM_CP_V6/"
#What is the job name
jobName = "CoPl_list_V6"
#Which string to grep for failing jobs
grepString = "Error"

#create the new cmd file with failing jobs
import subprocess
proc = subprocess.Popen(['grep '+grepString+' '+farmPATH+'logs/*.err'], stdout=subprocess.PIPE, shell=True)
(out, err) = proc.communicate()

print 'run:', 'grep '+grepString+' '+farmPATH+'logs/*.err'
print 'output is:'
print out

errList = out.split(farmPATH+'logs/')

jobList = []

for job in errList:
    if job=='' : continue
    jobList.append(job[:4])

print 'list of jobs to resubmit:', jobList

inCMDfile = open(farmPATH+'inputs/'+jobName+'.cmd','r')
inCMDstring = inCMDfile.read()

CMDs = inCMDstring.split('\n\n')

outCMDstring = CMDs[0]+'\n\n'+CMDs[1]+'\n\n'

for job in jobList:
    i = -1
    for CMD in CMDs:
        i += 1
        if i < 2 : continue
        if job in CMD:
            if not int(job)==i-2 : 'ERROR: job not matching', i
            else :
                if int(job)==i-2 : print 'looking for job:', job
                outCMDstring += CMD+'\n\n'
                break
print outCMDstring

outCMDfile = open(farmPATH+'inputs/failedJobs.cmd','w')
print 'output file is:'
print outCMDfile
print 'use "condor_submit" command to resubmit jobs'
outCMDfile.write(outCMDstring)
