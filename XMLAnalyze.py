# Author: Andrew Sainz
# 
# Purpose: XMLAnalyze is designed to iterate through a collection of Post data collected from Stack Overflow
# 		   forums. Data collected to analyze the code tagged information to find the language of the code
# 		   being utilized.
# 
# How to use: To run from command line input "python XMLAnalyze.py Posts.xml"

import sys
import re
import os
import nltk
import xml.etree.ElementTree as ET 
from nltk.util import ngrams
from ngramFunctions import *
from XMLParser import *
from frequencyFunctions import *

def features(sentence):
	words = sentence.lower().split()
	return dict(('contains(%s)' %w, True) for w in words)

if __name__ == '__main__':
	xmldoc = sys.argv[1]
	# comments = sys.argv[2]
	knownJava = sys.argv[2]
	# testFile = sys.argv[4]
	knownCpp = sys.argv[3]
###################################################################
# Section 1: Gather known data to create frequencies for known information
###################################################################
	knownJavaFile = open(knownJava)
	knownJavaString = ""
	for line in knownJavaFile:
		knownJavaString += line

	# knownJavaGram = ngramsFunction(knownJavaString, 3)
	knownJavaGram = ngrams(knownJavaString.split(' '),3)#ngramsFunction(knownJavaString, 3)
	knownJavaHashFreq = nltk.FreqDist(knownJavaGram)

	knownCPPFile = open(knownCpp)
	knownCPPString = ""
	for line in knownCPPFile:
		knownCPPString += line

	# print(knownCPPString)
	knownCPPGram = ngrams(knownCPPString.split(' '),3)
	knownCPPHashFreq = nltk.FreqDist(knownCPPGram)


###################################################################
# Section 2: Compare with known ngrams of code
###################################################################
	# myHash = createHash(xmldoc,comments)# createListOfCode(xmldoc)
	# print(len(myHash))




	# test = open(testFile)
	# testString = ""
	# for line in test:
	# 	testString += line

	# testString = os.linesep.join([s for s in testString.splitlines() if s])
	# testString = re.sub('\\n|\\r|/\s\s+/g}',' ',testString)
	# testString = re.sub('\.', ' ', testString)
	# testString = re.sub('\\t', '',testString)
	# testString = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,testString)
	# testString = re.sub(re.compile("//.*?\n" ) ,"" ,testString)
	# testString = re.sub( '[^0-9a-zA-Z]+', ' ', testString )
	# testString = re.sub( '\s+', ' ', testString ).strip()
	
	# testList = ngrams(testString.split(' '),3)
	# testGram = nltk.FreqDist(testList)

	# print(testString)

	
#############################################################################################
# Section to calculate trigram Probability
#############################################################################################
	kneserJava = nltk.KneserNeyProbDist(knownJavaHashFreq)
	kneserCPP = nltk.KneserNeyProbDist(knownCPPHashFreq)

	kneserJavaHash = convertProbListToHash(kneserJava)
	kneserCPPHash = convertProbListToHash(kneserCPP)
	
	cpp = 0
	java = 0

	outFile = open('Results.txt', 'a')

	tree = ET.parse(xmldoc)
	root = tree.getroot()

	for row in root:
		body = row.get('Body')
		# Only allow posts with a code tag to be added
		if '<code>' in body:
			postId = row.get('Id')
			# Tags for comment post
			tags = row.get('Tags')

			if tags == None:
				continue
			
			tags.lower()
			if not ('java' or 'c++') in tags:
				continue

			code = parseBodyForTagCode(body)
			codeString = ''
			for item in code:
				codeString = codeString+re.sub('<code>|</code>',' ',item)
			
			codeString = re.sub('\\n|\\r|/\s\s+/g}',' ',codeString)
			codeString = re.sub('\.', ' ', codeString)
			codeString = re.sub('\\t', '',codeString)
			codeString = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,codeString)
			codeString = re.sub(re.compile("//.*?\n" ) ,"" ,codeString)
			codeString = re.sub( '[^0-9a-zA-Z]+', ' ', codeString )
			codeString = re.sub( '\s+', ' ', codeString).strip()

			codeLength = len(codeString.split())

			if(codeLength < 3):
				continue

			codeList = ngrams(codeString.split(' '),3)
			codeGram = nltk.FreqDist(codeList)
			

			for gram in codeGram:
				cppValue = kneserCPPHash.get(str(gram))
				javaValue = kneserJavaHash.get(str(gram)) 

				if cppValue != None and javaValue != None:
					if cppValue > javaValue:
						cpp += 1
					else:
						java += 1
				elif cppValue == None and javaValue != None:
					java += 1
				elif cppValue != None and javaValue == None:
					cpp += 1

			fileString = ''
			fileString = fileString+'Grams assigned as followed:\n'
			fileString = fileString+'C++: {} Java: {}\n'.format(cpp,java)
			if cpp > java:
				fileString = fileString+'Code Snippet determined to be C++\nTags include {}\n'.format(tags)
			elif java > cpp:
				fileString = fileString+'Code Snippet determined to be Java\nTags include {}\n'.format(tags)
			elif java == cpp:
				fileString = fileString+'Code Snippet determined to be inconclusive\nTags include {}\n'.format(tags)

			outFile.write(fileString)