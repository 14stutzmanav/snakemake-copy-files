import pandas as pd
import shutil
import os
import re
import glob
import getpass
import sys
import argparse

configfile: './clusterConfig/slurmConfig.json'

########################

# def getTechReplicates(wildcards):
# 	"""
# 	Get the names of fastq files that will be concatenated together as technical replicates.
# 	Since data is paired-end, keep the read number in the file name.
# 	If there are no technical replicates, this simply cats the file to a new one w/ a different name
# 	"""
# 	readNumRegex = '_R{}'.format(wildcards.Num)

# 	# wildcards.tech is the prefix of the sample w/o the read number (1 or 2)
# 	techFilter = sampleDF [ sampleDF.techName == wildcards.tech ]
# 	fastqList = list(techFilter.fastqName)

# 	# we want to concatenate R1 technical reps and R2 technical reps seperately
# 	fastqList = [ fastqName for fastqName in fastqList 
# 			if re.search(readNumRegex, fastqName) ]

# 	# the fastq entry in the samplesheet does not contain the directory
# 	fastqList = [ 'Fastq/{}'.format(fastqName) for fastq in fastqList ]

# 	return(fastqList)

#########################

# Load Required Input Files:

# sampleSheetPath = str('master-samplesheet-hic.csv')
sampleSheetPath = str('master-samplesheet-faire.csv')

sampleDF = pd.read_csv(sampleSheetPath, comment = '#')

techList = list(set(sampleDF.techName))
fastqList= list(set(sampleDF.fastqName))
readNumList = list(sampleDF.readNum)


#########################
localrules: all

rule all:
	input:
		expand("../astutzman_faire/{fastq}.fastq.gz", fastq=fastqList)


rule copyFiles:
	input:
		lambda x: list(sampleDF.htsfFile)
	output:
		expand('../astutzman_faire/{fastq}.fastq.gz', fastq = list(sampleDF.fastqName))
	message: "Copying files to Fastq directory with corrected file names."
	run:
		for htsf in list(sampleDF.htsfFile):
			#print('HERE', htsf)
			outFileFilt = sampleDF [ sampleDF.htsfFile == htsf ] 
			outFileBase = list(outFileFilt.fastqName)[0]
			outFile = '../astutzman_faire/{fastq}.fastq.gz'.format(fastq = outFileBase)
			#print('THERE')
			#print(outFile)
			shutil.copyfile(htsf, outFile)
			print('copied file')

