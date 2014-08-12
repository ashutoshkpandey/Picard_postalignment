import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 2:	
	print "Usage: Input_directory Job_Script_directory" 
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

SAM = {}

for file in Listoffile:
	if file.endswith(".bam") and not os.path.getsize(file) == 0:
		if file not in SAM:
			SAM[file] = file.split("/")[-1]

#print SAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[2])):
        os.makedirs(str(Argument[2]))

for file in SAM:

	dirname = ""
	PU = ""

	info = []
	info = file.split("/")

	dirname = info[-1].rstrip(".bam")
	
	print file
	print info[-1]
	print dirname

	PU = dirname[dirname.find("_")+1:dirname.find("-")].split("_")[-1]
	
	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(dirname)+".sh")
	
	jobfile = open(str(jobname),"w")

	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=16\n#PBS -N Post_BAM_processing_"+str(dirname)+"\n\njava -jar -Xmx36g /home/apandey/bio/picard-tools-1.67/AddOrReplaceReadGroups.jar CREATE_INDEX=true MAX_RECORDS_IN_RAM=2000000 TMP_DIR=/scratch/  INPUT="+str(file)+" OUTPUT="+str(Argument[2])+"/"+str(SAM[file])+" SORT_ORDER=coordinate RGID="+str(dirname)+" RGLB=MatePair60x60  RGPL=SOLID  RGPU="+str(PU)+" RGSM=BXD29_WT  RGCN=MRC_UTHSC  RGDS=BXD29_WT_Genomic_sequencing_Williams_Lab_UTHSC\n")	
	jobfile.close()
	
	#print "qsub "+str(jobname)
	#os.system("qsub "+str(jobname))
