import os
import glob
import re

path = '/Documents/python/JavaExamples/'
gramHash = {}

for filename in glob.glob('*.java'):
	outFile = open('KnownJava.txt', 'a')
	fileOpen = open(filename, 'r', encoding='utf8', errors='ignore')
	fileString = ""

	for line in fileOpen:
		# Removes non ASCII characters 
		line = re.sub(r'[^\x00-\x7F]+',' ', line)

		try:
			fileString += line
		except:
			pass

	fileString = os.linesep.join([s for s in fileString.splitlines() if s])
	fileString = re.sub('\\n|\\r|/\s\s+/g}',' ',fileString)
	fileString = re.sub('\.', ' ', fileString)
	fileString = re.sub('\\t', '',fileString)
	fileString = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,fileString)
	fileString = re.sub(re.compile("//.*?\n" ) ,"" ,fileString)
	fileString = re.sub( '[^0-9a-zA-Z]+', ' ', fileString )
	fileString = re.sub( '\s+', ' ', fileString ).strip()


	outFile.write(fileString)
	fileOpen.close()