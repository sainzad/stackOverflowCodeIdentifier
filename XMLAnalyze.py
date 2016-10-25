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
from lxml import etree

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

	 # for event, element in etree.iterparse(posts_fn, tag="row"):
  #       ...

  #       element.clear()
  #       # Also eliminate now-empty references from the root node to elem
  #       for ancestor in element.xpath('ancestor-or-self::*'):
  #           while ancestor.getprevious() is not None:
  #               del ancestor.getparent()[0]

	
#############################################################################################
# Section to calculate trigram Probability
#############################################################################################
	kneserJava = nltk.KneserNeyProbDist(knownJavaHashFreq)
	kneserCPP = nltk.KneserNeyProbDist(knownCPPHashFreq)

	kneserJavaHash = convertProbListToHash(kneserJava)
	kneserCPPHash = convertProbListToHash(kneserCPP)
	 
	cpp = 0
	java = 0
	totalCppWithTag = 0
	totalJavaWithTag = 0
	totalEval = 0

	outFile = open('Results.txt', 'a')

	# tree = ET.parse(xmldoc)
	# root = tree.getroot()
	for event, element in etree.iterparse(posts_fn, tag="row"):
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
				if not ('java' or 'c++' or 'android' or 'spring' or 'swing') in tags:
					continue

				totalEval += 1# total posts not skipped

				code = parseBodyForTagCode(body)
				codeString = ''
				for item in code:
					codeString = codeString+re.sub('<code>|</code>',' ',item)
				
				codeString = re.sub('\n|\r|/\s\s+/g}',' ',codeString)
				codeString = re.sub('\.', ' ', codeString)
				codeString = re.sub('\t', '',codeString)
				codeString = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,codeString)
				codeString = re.sub(re.compile("//.*?\n" ) ,"" ,codeString)
				# codeString = re.sub( '[^0-9a-zA-Z]+', ' ', codeString )
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
				fileString = fileString+'PostId: {}\nC++: {} Java: {}\nCode: {} \n'.format(postId,cpp,java,codeString)
				if cpp > java:
					fileString = fileString+'Snippet determined to be C++\nTags include {}\n\n'.format(tags)
					if 'c++' in tags:
						totalCppWithTag += 1
				elif java > cpp:
					fileString = fileString+'Snippet determined to be Java\nTags include {}\n\n'.format(tags)
					if ('java' or 'android' or 'spring' or 'swing') in tags:
						totalJavaWithTag += 1
				elif java == cpp:
					fileString = fileString+'Snippet determined to be inconclusive\nTags include {}\n\n'.format(tags)
				
				java = 0
				cpp = 0

				outFile.write(fileString)
		element.clear()
		for ancestor in element.xpath('ancestor-or-self::*'):
			while ancestor.getprevious() is not None:
				del ancestor.getparent()[0]

	print('Total Java snippets with tags (java, android, spring, swing): {}'.format(totalJavaWithTag))
	print('Total C++ snippets with tags (c++): {}'.format(totalCppWithTag))
	print('Total snippets evaluated: {}'.format(totalEval))
