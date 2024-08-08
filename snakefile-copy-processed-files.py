import pandas as pd
import shutil
import os
import re
import glob
import getpass
import sys
import argparse

configfile: './clusterConfig/slurmConfig.json'

#########################

# Load Required Input Files:

# sampleSheetPath = str('master-samplesheet-hic.csv')
sampleSheetPath = str('master-samplesheet-processed-faire.csv')

sampleDF = pd.read_csv(sampleSheetPath, comment = '#')

newList= list(set(sampleDF.newName))

#########################
localrules: all

rule all:
	input:
		expand("../astutzman_faire/{new}", new=newList)


rule copyFiles:
	input:
		lambda x: list(sampleDF.originalFile)
	output:
		expand('../astutzman_faire/{new}', new = list(sampleDF.newName))
	message: "Copying files to new directory with corrected file names."
	run:
		for htsf in list(sampleDF.originalFile):
			#print('HERE', htsf)
			outFileFilt = sampleDF [ sampleDF.originalFile == htsf ] 
			outFileBase = list(outFileFilt.newName)[0]
			outFile = '{new}'.format(new = outFileBase)
			#print('THERE')
			#print(outFile)
			shutil.copyfile(htsf, outFile)
			print('copied file')

