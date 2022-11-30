import os 
import csv
import string
import pandas as pd

# Change directory to directory to check.

os.chdir("/data/output/results/")

# Directory list save in object 'name' to iterate through.


name = os.listdir()
dirname = []

for n in name:
	if n[0].isdigit():
		dirname.append(n)



print(dirname)



# Iterate through each directory name, check if the name has been altered or not, ammend the name and save all to new list 'namelist'

namelist = []
extra_list = []

for i in dirname:
	if i.count("_") > 3:
		i = i.rsplit("_", 1)
		start = i[0]
		end = i[-1]        # Use this again to extract the ending 
		namelist.append(str(start))
		almost = "_" + end
		extra_list.append(str(almost))        # Append the ending onto a new string

	else:
		namelist.append(str(i))
		extra_list.append(" ")	       # Append "None" to the new string to maintain the same number 
#print(namelist)

# Extract Year and See if it is in legacy folder

Legacylist = []

for n in namelist:
	year = n[0:2]
	newpath = "/data/archive/legacy-results/" + str(year)
	os.chdir(newpath)
	fullpath = newpath + "/" + n
	#print(fullpath) 
	exist = os.path.exists(fullpath)
	Legacylist.append(exist)
#print(Legacylist)


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




print(namelist)
print(extra_list)
print(Legacylist)
print(List)
print(List2)
#print(PipelineList)
#print(PanelList)


df= pd.DataFrame(list(zip(namelist, Legacylist, List, List2, extra_list)), columns = ["Run_ID", "In_Legacy", "Pipeline", "Panel", "Extra"])
df.to_csv("/home/v.ki282548/Wren_Run_ID_List", index = False)


print(df)