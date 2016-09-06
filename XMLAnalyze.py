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
from nltk.util import ngrams
from ngramFunctions import *
from XMLParser import *
from frequencyFunctions import *

def features(sentence):
	words = sentence.lower().split()
	return dict(('contains(%s)' %w, True) for w in words)

if __name__ == '__main__':
	xmldoc = sys.argv[1]
	comments = sys.argv[2]
	knownText = sys.argv[3]
	testFile = sys.argv[4]
###################################################################
# Section 1: Gather known data to create frequencies for known information
###################################################################
	knownJavaFile = open(knownText)
	knownJavaString = ""
	for line in knownJavaFile:
		knownJavaString += line

	# knownJavaGram = ngramsFunction(knownJavaString, 3)
	knownJavaGram = ngrams(knownJavaString.split(' '),3)#ngramsFunction(knownJavaString, 3)
	knownJavaHashFreq = nltk.FreqDist(knownJavaGram)

	# for key, value in knownJavaHash.items():
	# 	print(key)
	# 	print(value)

	# Shows frequency vs. total only towards known language
	# knownJavaFreq = createFrequencyHash(knownJavaGram)
	# for key, value in knownJavaFreq.items():
	# 	print(key)
	# 	print(value)


###################################################################
# Section 2: Compare with known ngrams of code
###################################################################
	# myHash = createHash(xmldoc,comments)# createListOfCode(xmldoc)
	# print(len(myHash))


	test = open(testFile)
	testString = ""
	for line in test:
		testString += line

	testString = os.linesep.join([s for s in testString.splitlines() if s])
	testString = re.sub('\\n|\\r|/\s\s+/g}','',testString)
	testString = re.sub(' +|.', ' ', testString)

	testList = ngrams(testString.split(' '),3)
	testGram = nltk.FreqDist(testList)

	for key, value in testGram.items():
		if knownJavaHashFreq.get(key) != None:
			print(calculateFrequency(int(knownJavaHashFreq.get(key)),value))
			print(key)
	# Holds ngram of posts.xml file
	# gramHash = createNgramHash(myHash,3)
	# print(len(gramHash))

	# for key,value in gramHash.items():
	# 	print(key)

	# freqHash = createFrequencyHash(gramHash)
	# print(len(freqHash))

	# for key,value in freqHash.items():
	# 	try:
	# 		if value > .00018:
	# 			print(key)
	# 			print (value)
	# 	except:
	# 		pass