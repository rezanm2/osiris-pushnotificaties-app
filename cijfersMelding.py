import requests
import re
import pypandoc
import time
import docx2txt
import datetime


teZoekenVakken = [['Logica', '16-04-2019'], ['IWIS', '18-04-2019'], ['Sensor', '15-04-2019']]
gedaan = [False]*len(teZoekenVakken)
oudeRijen = []
url = "https://mijnApi"

while True:

	print('Voor de check: ', 'ILG1:', gedaan[0], 'IWIS:', gedaan[1])
	output = pypandoc.convert(source='/Users/rnaser/Downloads/OSIRIS - Resultaten.html', format='html', to='docx', outputfile='/Users/rnaser/Downloads/OSIRIS - Resultaten.docx')
	time.sleep(5)
	def validate(date_string):
		date_format = '%d-%m-%Y'
		try:
		  date_obj = datetime.datetime.strptime(date_string, date_format)
		  return True
		except ValueError:
		  return False

	text = docx2txt.process("/Users/rnaser/Downloads/OSIRIS - Resultaten.docx")

	file = open("testfile.txt", "w")

	file.write(text)
	file.close()
	time.sleep(2)

	F = open('testfile.txt', 'r')
	ga = False
	counter = 0
	datumNr = 0
	tekst = ""
	for line in F:
		if validate(line.strip()):
			counter += 1
			ga = True
			if datumNr == 2:
				datumNr = 0
			datumNr += 1
		while ga:
			if line not in ['\n', '\r\n'] and counter < 30:

				if datumNr == 1:
					tekst = tekst + line.strip() + "; "
				if datumNr == 2:
					tekst = tekst + "\n"
			break
	F.close()

	file = open("lijstCijfers.txt", "w")
	file.write(tekst)
	file.close()
	time.sleep(2)

	allesInArray = []
	cijfers = open('lijstCijfers.txt', 'r')
	for regel in cijfers:
		regel = regel.strip()
		allesInArray.append(regel.split(";"))
	if oudeRijen is not 0:
		for rij in allesInArray:
			for nieuw in oudeRijen:
				if rij[0] == nieuw[0] and rij[1] == nieuw[1] and 'concept' not in rij[5]:
					requests.post(url + rij[1].strip()+'=definitief.')

	#print(len(allesInArray))
	for zoeken in allesInArray:
		for eenVak in range(len(teZoekenVakken)):
			if (teZoekenVakken[eenVak][0] and teZoekenVakken[eenVak][1]) in zoeken and gedaan[eenVak] == False:
				gedaan[eenVak] = True
				requests.post((url + zoeken[1].strip()+'=' + zoeken[5].replace(" ", "")))

	print('Na check: ', 'ILG1:', gedaan[0], 'IWIS:', gedaan[1])
	oudeRijen = []
	for dd in allesInArray:
		if 'concept' in dd[5]:
			oudeRijen.append(dd)
			print('-----: ', dd)
	time.sleep(30)






