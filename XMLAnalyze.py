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
###################################################################
# Section 1: Gather known data to create frequencies for known information
###################################################################
	knownJavaFile = open(knownText)
	knownJavaString = ""
	for line in knownJavaFile:
		knownJavaString += line

	knownJavaString = os.linesep.join([s for s in knownJavaString.splitlines() if s])
	knownJavaString = re.sub('\\n|\\r|/\s\s+/g}','',knownJavaString)
	knownJavaString = re.sub(' +', ' ', knownJavaString)
	# print(knownJavaString)
	knownJavaGram = ngramsFunction(knownJavaString, 3)
	# knownJavaList = ngrams(knownJavaString.split(' '),3)#ngramsFunction(knownJavaString, 3)
	# for gram in knownJavaList:
		# knownJavaGram.update({gram});
	# for key, value in knownJavaGram.items():
	# 	print(key)
	# 	print(value)

	knownJavaFreq = createFrequencyHash(knownJavaGram)
	for key, value in knownJavaFreq.items():
		print(key)
		print(value)


###################################################################
# Section 2: Compare with known ngrams of code
###################################################################
	# myHash = createHash(xmldoc,comments)# createListOfCode(xmldoc)
	# print(len(myHash))

	# javaSearchTerms = ['java','system.out','enum']
	# gatherKnownJava = gatherKnown(myHash, javaSearchTerms)
	# print(len(gatherKnownJava))

	# for key, value in gatherKnownJava.items():
	# 	print(key)

	# gramHash = createNgramHash(myHash,3)
	# print(len(gramHash))

	# for key,value in gramHash.items():
	# 	try:
	# 		if value > 1:
	# 			print(key)
	# 	except:
	# 		pass

	# freqHash = createFrequencyHash(gramHash)
	# print(len(freqHash))

	# for key,value in freqHash.items():
	# 	try:
	# 		if value > .00018:
	# 			print(key)
	# 			print (value)
	# 	except:
	# 		pass