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

SAM = {}

for Filepath in Listoffile:
	for (path, dirs, files) in os.walk(Filepath):
		for file in files:
			if file.endswith(".sam") and not os.path.getsize(path+"/"+file) == 0:
				if path+"/"+file not in SAM:
					SAM[path+"/"+file] = (path+"/"+file).replace(".sam",".sam")

#print SAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[2])):
        os.makedirs(str(Argument[2]))

for file in SAM:
	dirname = ""

	info = []
	info = file.split("/")

	dirname = info[-2]

	if not os.path.exists(str(Argument[2])+"/"+str(dirname)):
		 os.makedirs(str(Argument[2])+"/"+str(dirname))

	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(dirname)+"_sam.sh")
	jobfile = open(str(jobname),"w")

	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=4\n#PBS -N Clean_SAM_processing_"+str(dirname)+"\n\njava -jar -Xmx9g /home/apandey/bio/picard-tools-1.67/CleanSam.jar VALIDATION_STRINGENCY=STRICT  TMP_DIR=/scratch/  INPUT="+str(file)+"  OUTPUT="+str(Argument[2])+"/"+str(dirname)+"/"+str(SAM[file].split("/")[-1]))	
	jobfile.close()
	
	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))
