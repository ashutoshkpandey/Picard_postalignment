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

for Filepath in Listoffile:
	if Filepath.endswith(".bam") and not os.path.getsize(Filepath) == 0:
		if Filepath not in SAM:
                	SAM[Filepath] = (Filepath).replace(".bam",".bam")	
"""
	for (path, dirs, files) in os.walk(Filepath):
		for file in files:
			if file.endswith(".bam") and not os.path.getsize(path+"/"+file) == 0:
				if path+"/"+file not in SAM:
					SAM[path+"/"+file] = (path+"/"+file).replace(".bam",".bam")
"""

print SAM
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

for file in SAM:
	dirname = ""

	info = []
	info = file.split("/")

	dirname = info[-1]

	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(dirname)+"_sam.sh")
	jobfile = open(str(jobname),"w")

	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=4\n#PBS -N Estimate_insert_size_"+str(dirname)+"\n\njava -jar -Xmx10g /home/apandey/bio/picard-tools-1.67/CollectInsertSizeMetrics.jar VALIDATION_STRINGENCY=LENIENT  DEVIATIONS=5  MINIMUM_PCT=0.1  METRIC_ACCUMULATION_LEVEL=READ_GROUP  HISTOGRAM_FILE=/home/apandey/"+str(dirname)+".hist  TMP_DIR=/scratch/ REFERENCE_SEQUENCE=/home/apandey/Reference_Fasta/mm10/mm10_ucsc/mm10_ucsc.fa  INPUT="+str(file)+"  OUTPUT=/home/apandey/"+str(dirname)+".out")	
	jobfile.close()
	
	#jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=8\n#PBS -N Building_index"+str(dirname)+"\n\n/home/apandey/bio/samtools-0.1.18/samtools index "+str(file))
 	#jobfile.close()

	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))
