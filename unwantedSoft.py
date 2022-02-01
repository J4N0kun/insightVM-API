# Purpose:
# 	This script generates a JSON association of software -> hostname
# 	I use this script to find unwanted software present on my servers
# 
# Dependance:
# 	connIVM.py -> to connect to insightVM API (Fill-in your credentials within this script)
#	assetList.py -> output of assetList.py is the input of this script
#
# Usage:
# 	1) Fill-in the UNWANTED_SOFT list below (not case sensitive and the matching is not done on the whole soft name).
#	   You may want to use softwareList.py script to have a complete list of the software found on all your assets by insightVM.
# 	2) Run the assetList.py script that will generate a flat file of all installed software per assetList
# 	3) Run this script to parse the asseList.json file created by assetList.py
# 	4) unwantedSoft.json file and unwantedSoft.csv file are generated
# 	5) Review your results
#
# Output:
#	A Json file and a CSV file.


import json, os

FILE = "assetList.json"
RESULT_FILE_JSON = "unwantedSoft.json"
RESULT_FILE_CSV = "unwantedSoft.csv"

UNWANTED_SOFT = ["Adobe Reader", "Adobe Acrobat Reader", "Adobe PDF Reader", "Adobe AIR", "Adobe Flash", "Foxit", "LogMeIn", "Malwarebytes",
				 "Microsoft Office", "Silverlight", "Mozilla Firefox", "TeamViewer", "VideoLAN", "WebEx", "Wireshark"]

class Software:
        def __init__(self, softname, serverList=[]):
                self.softname = softname
                self.serverList = serverList
        def toCSV(self):
                return self.softname + ";"  + "".join([str(server) + ";" for server in self.serverList]) + "\n"
				 
result = []
with open(FILE) as f:
	data = json.load(f)
for uwSoft in UNWANTED_SOFT:
	serverList = []
	for server in data["serverList"]:
		for soft in server["softList"]:
			if soft.lower().find(uwSoft.lower()) != -1:
				serverList.append(server["hostname"])
	if len(serverList) > 0:
		result.append(Software(uwSoft, serverList))
	serverList = []
if os.path.isfile(RESULT_FILE_JSON):
	os.remove(RESULT_FILE_JSON)
with open(RESULT_FILE_JSON,"a") as f:
	f.write(json.dumps(result, default=lambda o: o.__dict__, sort_keys=True, indent=4))
print(RESULT_FILE_JSON+ " has been created.")

if os.path.isfile(RESULT_FILE_CSV):
	os.remove(RESULT_FILE_CSV)
with open(RESULT_FILE_CSV,"a") as f:
	for s in result:
		f.write(str(s.toCSV()))
print(RESULT_FILE_CSV + " has been created.")