# Author: Andrew Sainz
# 
# Purpose: XMLAnalyze is designed to iterate through a collection of Post data collected from Stack Overflow
# 		   forums. Data collected to analyze the code tagged information to find the language of the code
# 		   being utilized.
# 
# How to use: To run from command line input "python XMLAnalyze.py Posts.xml"

import sys
import re
from ngramFunctions import *
from XMLParser import *
from frequencyFunctions import *

def features(sentence):
	words = sentence.lower().split()
	return dict(('contains(%s)' %w, True) for w in words)

if __name__ == '__main__':
	xmldoc = sys.argv[1]
	comments = sys.argv[2]

	myHash = createHash(xmldoc,comments)# createListOfCode(xmldoc)
	# print(len(myHash))

	javaSearchTerms = ['java','system.out','enum']
	gatherKnownJava = gatherKnown(myHash, javaSearchTerms)
	print(len(gatherKnownJava))

	# for key, value in gatherKnownJava.items():
	# 	print(key)

	gramHash = createNgramHash(myHash,3)
	# print(len(gramHash))

	# for key,value in gramHash.items():
	# 	try:
	# 		if value > 1:
	# 			print(key)
	# 	except:
	# 		pass

	freqHash = createFrequencyHash(gramHash)
	# print(len(freqHash))

	# for key,value in freqHash.items():
	# 	try:
	# 		if value > .00018:
	# 			print(key)
	# 			print (value)
	# 	except:
	# 		pass