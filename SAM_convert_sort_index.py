import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 2:	
	print "Usage: Input_directory Job_Script_directory Header-info(file) Output_directory" 
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

for Filepath in Listoffile:
	for (path, dirs, files) in os.walk(Filepath):
		for file in files:
			if file.endswith(".bam") and not os.path.getsize(path+"/"+file) == 0:
				print file
				if path+"/"+file not in SAM:
					SAM[path+"/"+file] = (path+"/"+file)

#.replace(".sam",".bam")

#print SAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[3])):
        os.makedirs(str(Argument[3]))

Header = {}

for line in fileinput.input([Argument[2]]):
        if line.startswith("#") or not line.strip():
                continue
        array = []
        line = line.rstrip("\n")
        array = line.split("\t")
	if array[3] not in Header:
		Header[array[3]] = array
		
PU = 0

for file in SAM:
	dirname = ""
	PU = PU + 1

	info = []
	info = file.split("/")

	dirname = info[-1].split("-")[0]
	#PU = file.split("_")[-1].replace(".sam","")

	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(dirname)+"_bam.sh")
	
	jobfile = open(str(jobname),"w")

	print dirname

	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=8\n#PBS -N Post_SAM_processing_"+str(dirname)+"\n\njava -jar -Xmx20g  /home/apandey/bio/picard-tools-1.67/AddOrReplaceReadGroups.jar CREATE_INDEX=true MAX_RECORDS_IN_RAM=5000000  VALIDATION_STRINGENCY=LENIENT   TMP_DIR=/scratch/   INPUT="+str(file)+"  OUTPUT="+str(Argument[3])+"/"+str(SAM[file].split("/")[-1])+"  SORT_ORDER=coordinate  RGID="+str(dirname)+"  RGLB="+str(Header[dirname][7])+"  RGPL="+str(Header[dirname][5])+"  RGPU="+str(PU)+" RGSM=DBA2_J  RGCN=UTHSC  RGDS=DBA2_J_UTHSC_SOLiD_mate_pair\n")	
	jobfile.close()
	
	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))
