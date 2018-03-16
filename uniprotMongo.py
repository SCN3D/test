#!/usr/bin/python
import pymongo
from pymongo import MongoClient
import sys
import os.path


#*.py -l filepath -db dbname -col collection_name -f [go,interpro,pfam,prosite,smart,supfam] or all
# *.py -o -db dbname -col collection_name -f [go,interpro,pfam,prosite,smart,supfam] or all
# count the arguments
arguments = len(sys.argv) - 1  
filepath = ''
features = {
	'go' : 0,'interpro' : 0,'pfam' : 0,'prosite' : 0,'smart' : 0,'supfam' : 0
}
dbname = ''
colname = ''
if arguments > 6 and arguments < 13 and sys.argv[1] == "-o" and sys.argv[2] == "-db" and sys.argv[4] == "-col" and sys.argv[6] == "-f":
	input("online download")
	if sys.argv[7] == 'all':
		features = {'go' : 1,'interpro' : 1,'pfam' : 1,'prosite' : 1,'smart' : 1,'supfam' : 1}
	else:
		for i in range(7,arguments):
			features[sys.argv[i]] = 1
	dbname = sys.argv[3]
	colname = sys.argv[5]
elif arguments > 7 and arguments < 14 and sys.argv[1] == "-l" and sys.argv[3] == "-db" and sys.argv[5] == "-col" and sys.argv[7] == "-f":
	if os.path.exists(sys.argv[2]):
		# file exists
		filepath = sys.argv[2]
	else:
		input("File does not exist\n")
		sys.exit()
	if sys.argv[8] == 'all':
		features = {'go' : 1,'interpro' : 1,'pfam' : 1,'prosite' : 1,'smart' : 1,'supfam' : 1}
	else:
		for i in range(8,arguments):
			features[sys.argv[i]] = 1
	dbname = sys.argv[4]
	colname = sys.argv[6]
else:
	input("Syntax:\nLocal file update: *.py -l filepath -db dbname -col collection_name -f [go,interpro,pfam,prosite,smart,supfam]\nOnline update: *.py -o -db dbname -col collection_name -f [go,interpro,pfam,prosite,smart,supfam]\n")
	sys.exit()

#connect to mongodb
client = MongoClient('localhost', 27017)
# Get the database
db = client[dbname]
collections = db[colname]

# Open a file
id_flag = 0
ac_flag = 0
sequence = ''

out_data = dict()
with open(filepath) as fp:
	for line in fp:
		collapsed = ' '.join(line.split())
		data = collapsed.split(";")
		parsed_1 = data[0].split(" ")
		if parsed_1[0] == "ID" and  id_flag == 0:
			id_flag = 1
			out_id = parsed_1[1]
			
		elif parsed_1[0] == "AC" and  ac_flag == 0:
			ac_flag = 1	
			out_ac.append(parsed_1[1])
			if len(data)  > 2:
				for x in range(1, len(data)-1):
					out_ac.append(data[x])
			out_data = {'_id' : out_id,'ac':out_ac}
		elif len(parsed_1[0]) > 2:
			sequence += collapsed
		##go numbers
		elif parsed_1[0] == "DR" and  parsed_1[1].lower() in features:
			if features[parsed_1[1].lower()] == 1:
				parsed_2 = data[1].split(" ")
				#out.append( parsed_2[1])
				if parsed_1[1].lower() in out_data:
					out_data[parsed_1[1].lower()].append(parsed_2[1])
				else:
					out_data[parsed_1[1].lower()] = [parsed_2[1]]
		##
		
			
		##
		elif parsed_1[0] == '//':
			sequence = ''.join(sequence.split())
			
			out_data['sequence'] = sequence
			collections.save(out_data)
			input("Enter to continue")
			##rewind
			id_flag = 0
			ac_flag = 0
			out_ac = []
			out_go = []
			out_interpro = []
			out_pfam = []
			out_prosite = []
			out_smart = []
			out_supfam = []
			sequence = '';
		
fp.close()
input("Enter to close")
	