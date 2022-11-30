# Load anaconda and import all relevant modules needed for this script

import os 
import csv
import string
import pandas as pd

# Changing Directory to RunID List

os.chdir("/data/output/results/")

# Save Directories into a List 
name = os.listdir()

#Loop to go through List and check they all start with a number, if not then they arent added to the final list.

dirname = []

for n in name:
	if n[0].isdigit():
		dirname.append(n)


# Iterate through each name in list, count number of "_" in name and split name if more than 3 are counted. 

namelist = []
extra_list = []

for i in dirname:
	if i.count("_") > 3:
		start = "_".join(i.split("_", 4)[:4])      # Splits and stores the first half of the name for RUN_ID List
		end = "_".join(i.split("_", 4)[4:])        # Splits and stores the second half od the name for EXTRA List
		namelist.append(str(start))
		almost = "_" + end
		extra_list.append(str(almost))        

	else:
		namelist.append(str(i))        # If "_" not > 3, name added straight to RUN_ID List and empty string added to EXTRA List
		extra_list.append(" ")	       

# Extract Year from first 2 characters of RUN_ID name and use that to move into the correct directory within the legacy-results directory.
# True or False statement saved for each RUN_ID on whether the same directory was found in the relevant directory within legacy-results

Legacylist = []

for n in namelist:
	year = n[0:2]
	newpath = "/data/archive/legacy-results/" + str(year)
	os.chdir(newpath)
	fullpath = newpath + "/" + n
	#print(fullpath) 
	exist = os.path.exists(fullpath)
	Legacylist.append(exist)                             


# Iterate through each directory name in RUN_ID list. The 8th character is checked to reveal which sequencer directory to look within.
# Within that it then checks to see if the SampleSheet.csv is there and if so, reads through each line until one line contains "pipe" string.
# This is then cleaned with all empty strings removed and then the final string is selected as this contains all relevant info.
# Split at ";" as this separated pipe and panel infor and then each is extracted and saved to a Pipeline List and Panel List.

# This is iterated over Novaseg, Miseq and Nextseq


pipe = "pipelineName="
panel = "panel="

PipelineList = []
PanelList = []


for n in namelist:
	sequencer = n[7]
	if sequencer == "A":
		seqpath = "/data/archive/novaseq/" + n + "/SampleSheet.csv"
		if os.path.exists(seqpath) == True:
			with open(seqpath) as file:
				read = csv.reader(file, delimiter=",")
				for row in read:
					row2 = list(filter(None, row))
					if pipe in str(row2):
						PipeCheck = row2[-1]
						PanelCheck = row2[-1]
						break
				if pipe in PipeCheck:
					PipeCheck = PipeCheck.split(";")
					PipelineList.append(PipeCheck[0])
				else:
					PipelineList.append("NO PIPELINE")
				if panel in PanelCheck:
					PanelCheck = PanelCheck.split(";")
					PanelList.append(PanelCheck[2])
				else:
					PanelList.append("NO PANEL")
		else:
			PipelineList.append("NO SAMPLESHEET")
			PanelList.append("NO SAMPLESHEET")



	if sequencer == "M":
		seqpath = "/data/archive/miseq/" + n + "/SampleSheet.csv"
		if os.path.exists(seqpath) == True:
			with open(seqpath) as file:
				read = csv.reader(file, delimiter=",")
				for row in read:
					row2 = list(filter(None, row))
					if pipe in str(row2):
						PipeCheck = row2[-1]
						PanelCheck = row2[-1]
						break
				if pipe in PipeCheck:
					PipeCheck = PipeCheck.split(";")
					PipelineList.append(PipeCheck[0])
				else:
					PipelineList.append("NO PIPELINE")
				if panel in PanelCheck:
					PanelCheck = PanelCheck.split(";")
					PanelList.append(PanelCheck[2])
				else:
					PanelList.append("NO PANEL")
		else:
			PipelineList.append("NO SAMPLESHEET")
			PanelList.append("NO SAMPLESHEET")



	if sequencer == "N":
		seqpath = "/data/archive/nextseq/" + n + "/SampleSheet.csv"
		if os.path.exists(seqpath) == True:
			with open(seqpath) as file:
				read = csv.reader(file, delimiter=",")
				for row in read:
					row2 = list(filter(None, row))
					if pipe in str(row2):
						PipeCheck = row2[-1]
						PanelCheck = row2[-1]
						break
				if pipe in PipeCheck:
					PipeCheck = PipeCheck.split(";")
					PipelineList.append(PipeCheck[0])
				else:
					PipelineList.append("NO PIPELINE")
				if panel in PanelCheck:
					PanelCheck = PanelCheck.split(";")
					PanelList.append(PanelCheck[2])
				else:
					PanelList.append("NO PANEL")
		else:
			PipelineList.append("NO SAMPLESHEET")
			PanelList.append("NO SAMPLESHEET")


# Remove the pipe and panel prefix from each entry.

List = []
List2 = []

for entry in PipelineList:
	if pipe in entry:
		List.append(entry.replace("pipelineName=", ""))
	else:
		List.append(entry)

for entry in PanelList:
	if panel in entry:
		List2.append(entry.replace("panel=", ""))
	else:
		List2.append(entry)

# Convert lists into dataframe and then write to csv.

df= pd.DataFrame(list(zip(namelist, Legacylist, List, List2, extra_list)), columns = ["Run_ID", "In_Legacy", "Pipeline", "Panel", "Extra"])
df.to_csv("/home/v.ki282548/Wren_Run_ID_List", index = False)


print(df)