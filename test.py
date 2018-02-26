#!/usr/bin/python

# Open a file
id_flag = 0
ac_flag = 0
sequence = ''
out_go = []
out_interpro = []
out_pfam = []
out_prosite = []
out_smart = []
out_supfam = []
with open('test2.txt') as fp:
	for line in fp:
		collapsed = ' '.join(line.split())
		data = collapsed.split(";")
		parsed_1 = data[0].split(" ")
		if parsed_1[0] == "ID" and  id_flag == 0:
			id_flag = 1
			print('id: ',parsed_1[1])
			out_id = parsed_1[1]
		elif parsed_1[0] == "AC" and  ac_flag == 0:
			ac_flag = 1
			print('ac 1: ',parsed_1[1])
			out_ac = parsed_1[1]
			if len(data)  > 2:
				for x in range(1, len(data)-1):
					print('ac', x+1,': ', data[x])
					out_ac += data[x]
		elif len(parsed_1[0]) > 2:
			sequence += collapsed
		##go numbers
		elif parsed_1[0] == "DR" and  parsed_1[1] == "GO":
			parsed_2 = data[1].split(" ")
			out_go.append( parsed_2[1])
			print('GO:  ',parsed_2[1])
		##
		##interpro
		elif parsed_1[0] == "DR" and  parsed_1[1] == "InterPro":
			parsed_2 = data[1].split(" ")
			out_interpro.append( parsed_2[1])
			print('interPro:  ',parsed_2[1])
		##
		##pfam
		elif parsed_1[0] == "DR" and  parsed_1[1] == "Pfam":
			parsed_2 = data[1].split(" ")
			out_pfam.append(parsed_2[1])
			print('Pfam:  ',parsed_2[1])
		##
		##prosite
		elif parsed_1[0] == "DR" and  parsed_1[1] == "PROSITE":
			parsed_2 = data[1].split(" ")
			out_prosite.append( parsed_2[1])
			print('Prosite:  ',parsed_2[1])
		##
		##smart
		elif parsed_1[0] == "DR" and  parsed_1[1] == "SMART":
			parsed_2 = data[1].split(" ")
			out_smart.append(parsed_2[1])
			print('SMART:  ',parsed_2[1])
		##
		##supfam
		elif parsed_1[0] == "DR" and  parsed_1[1] == "SUPFAM":
			parsed_2 = data[1].split(" ")
			out_supfam.append(parsed_2[1])
			print('SUPFAM:  ',parsed_2[1])
		##
		elif parsed_1[0] == '//':
			sequence = ''.join(sequence.split())
			data = {'id': out_id, 'ac': out_ac, 'go': out_go,'interpro':out_interpro,'pfam':out_pfam,
			'prosite': out_prosite,'smart': out_smart,'supfam': out_supfam,'sequence': sequence}
			print(data)
			##rewind
			id_flag = 0
			ac_flag = 0
			out_go = []
			out_interpro = []
			out_pfam = []
			out_prosite = []
			out_smart = []
			out_supfam = []
			sequence = '';
		
fp.close()
        
             
            
        
         
