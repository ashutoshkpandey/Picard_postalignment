import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 2:	
	print "Usage: Input_directory Job_Script_directory Output_directory" 
	sys.exit()
  
dpath = Argument[0]
Listoffile = []

def dir(patharray):
    Listdir = []
    for infile in patharray:
        Listdir.append(os.path.join(dpath,infile))
    return Listdir    

Listoffile = dir(os.listdir(dpath))
#print Listoffile

BAM = {}

for file in Listoffile:
	if file.endswith(".bam") and not os.path.getsize(file) == 0:
		if file not in BAM:
			BAM[file] = file.split("/")[-1]

#print BAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[2])):
        os.makedirs(str(Argument[2]))

for file in BAM:

	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(BAM[file])+".sh")
	
	jobfile = open(str(jobname),"w")

	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=16\n#PBS -N Mark_Duplicates_"+str(BAM[file])+"\n\njava -jar -Xmx40g /home/apandey/bio/picard-tools-1.67/MarkDuplicates.jar  CREATE_INDEX=true  VALIDATION_STRINGENCY=LENIENT  MAX_RECORDS_IN_RAM=2000000 TMP_DIR=/scratch/  INPUT="+str(file)+" OUTPUT="+str(Argument[2])+"/"+str(BAM[file])+"  METRICS_FILE="+str(Argument[1])+"/"+str(BAM[file])+"_metric.txt  ASSUME_SORTED=true  REMOVE_DUPLICATES=false  MAX_FILE_HANDLES_FOR_READ_ENDS_MAP=4000")	
	jobfile.close()
	
	print "qsub "+str(jobname)
	#os.system("qsub "+str(jobname))
