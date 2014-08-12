import os, glob
import sys,re,fileinput

Argument = []
Argument = sys.argv[1:] 

if (len(Argument)) < 4:	
	print "Usage: Bam_files_directory Job_Script_directory Library-info(file) Output_directory" 
	sys.exit()
  
def dir(patharray):
    Listdir = []
    for infile in patharray:
        Listdir.append(os.path.join(dpath,infile))
    return Listdir    
									
if not os.path.exists(str(Argument[1])):
	os.makedirs(str(Argument[1]))

if not os.path.exists(str(Argument[3])):
        os.makedirs(str(Argument[3]))

Library = {}

for line in fileinput.input([Argument[2]]):
        if line.startswith("#") or not line.strip() or line.startswith("Study"):
                continue
        array = []
        line = line.rstrip("\n")
        array = line.split("\t")

	if array[7] not in Library:
		Library[array[7]] = []
		if array[0]+".bam" not in Library[array[7]]:
			Library[array[7]].append(array[0]+".bam")
	else:
		if array[0]+".bam" not in Library[array[7]]:
                	Library[array[7]].append(array[0]+".bam")
		
"""
		if array[13].endswith("_1.fastq.gz"):
			if array[13].replace("_1.fastq.gz",".bam") not in Library[array[7]]:
				Library[array[7]].append(array[13].replace("_1.fastq.gz",".bam"))
		if array[13].endswith("_2.fastq.gz"):
                        if array[13].replace("_2.fastq.gz",".bam") not in Library[array[7]]:
                                Library[array[7]].append(array[13].replace("_2.fastq.gz",".bam"))
	else:
		if array[13].endswith("_1.fastq.gz"):
                        if array[13].replace("_1.fastq.gz",".bam") not in Library[array[7]]:
                                Library[array[7]].append(array[13].replace("_1.fastq.gz",".bam"))
                if array[13].endswith("_2.fastq.gz"):
                        if array[13].replace("_2.fastq.gz",".bam") not in Library[array[7]]:
                                Library[array[7]].append(array[13].replace("_2.fastq.gz",".bam"))
"""
#print Library.values()

	
for library in Library:

	dirname = ""
	dirname = library
	inputstring = ""
	Bam_list = []

	if len(Library[library]) == 1:
		print ("cp "+str(Argument[0])+"/"+str(Library[library][0])+"  "+str(Argument[3])+"/"+str(library)+".bam")
		os.system("cp "+str(Argument[0])+"/"+str(Library[library][0])+"  "+str(Argument[3])+"/"+str(library)+".bam")
		os.system("cp "+str(Argument[0])+"/"+str((Library[library][0]).replace(".bam",".bai"))+"  "+str(Argument[3])+"/"+str(library)+".bai")
		continue
	
	for fastq in Library[library]:
		inputstring = inputstring + "INPUT="+Argument[0]+"/"+str(fastq)+"   "
	
	#print inputstring

	jobname = ""
	jobname = str(Argument[1])+"/"+re.sub(r'\s','',str(library)+"_merge_bams.sh")
	jobfile = open(str(jobname),"w")
	
	jobfile.write("#!/bin/bash\n#PBS -l walltime=240:00:00\n#PBS -l nodes=1:ppn=16\n#PBS -N BAM_merging_"+str(dirname)+"\n\njava -jar -Xmx36g /home/apandey/bio/picard-tools-1.67/MergeSamFiles.jar  CREATE_INDEX=true MAX_RECORDS_IN_RAM=9000000 VALIDATION_STRINGENCY=LENIENT  TMP_DIR=/scratch/ "+str(inputstring)+"   OUTPUT="+str(Argument[3])+"/"+str(library)+".bam  SORT_ORDER=coordinate  ASSUME_SORTED=true  USE_THREADING=true")

	jobfile.close()
	
	print "qsub "+str(jobname)
	os.system("qsub "+str(jobname))



