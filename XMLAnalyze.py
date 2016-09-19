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
	knownCpp = sys.argv[5]
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

	knownCPPFile = open(knownCpp)
	knownCPPString = ""
	for line in knownCPPFile:
		knownCPPString += line

	# print(knownCPPString)
	knownCPPGram = ngrams(knownCPPString.split(' '),3)
	knownCPPHashFreq = nltk.FreqDist(knownCPPGram)

	# for key, value in knownCPPHashFreq.items():
	# 	print(key)


	# for key, value in knownJavaHashFreq.items():
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
	testString = re.sub('\\n|\\r|/\s\s+/g}',' ',testString)
	testString = re.sub(' +|\.', ' ', testString)
	testString = re.sub( '\s+', ' ', testString ).strip()
	
	testList = ngrams(testString.split(' '),3)
	testGram = nltk.FreqDist(testList)


#############################################################################################
# This is where a comparison of frequencies vs. ngram will be made. 
# The higher the frequency language gram will be selected and added towards langauge total. 
#############################################################################################
	totalCpp = 0
	totalJava = 0

	for key, value in testGram.items():
		# print(key)
		if(knownJavaHashFreq.get(key) == None and knownCPPHashFreq.get(key) != None):
			# print('C++')
			totalCpp += 1
		if(knownJavaHashFreq.get(key) != None and knownCPPHashFreq.get(key) == None):
			# print('java')
			totalJava += 1
		if knownJavaHashFreq.get(key) != None and knownCPPHashFreq.get(key) != None:
			javaFreq = calculateFrequency(int(knownJavaHashFreq.get(key)),value)
			cppFreq = calculateFrequency(int(knownCPPHashFreq.get(key)), value)

			if(javaFreq > cppFreq):
				# print('java')
				totalJava += 1
			else:
				# print('C++')
				totalCpp += 1
		# print(key)

	print('C++ tags: {}'.format(totalCpp))
	print('Java tags: {}'.format(totalJava))
			# print(knownJavaHashFreq.get(key))
			# print(calculateFrequency(int(knownJavaHashFreq.get(key)),value))
			# print(key)