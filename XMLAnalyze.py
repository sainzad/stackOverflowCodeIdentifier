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

	myList = createListOfCode(xmldoc)
	# print(myList)

	gatherKnownJava = gatherKnownTags(myList, 'java')
	print(gatherKnownJava)

	gramHash = createNgramHash(myList,3)
	# print(gramHash)

	freqHash = createFrequencyHash(gramHash)
	# print(freqHash)

