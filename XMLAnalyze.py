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
import operator
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

	# javaMaxGram = max(knownJavaHashFreq, key=knownJavaHashFreq.get)
	# print(javaMaxGram, knownJavaHashFreq[javaMaxGram])

	knownCPPFile = open(knownCpp)
	knownCPPString = ""
	for line in knownCPPFile:
		knownCPPString += line

	# print(knownCPPString)
	knownCPPGram = ngrams(knownCPPString.split(' '),3)
	knownCPPHashFreq = nltk.FreqDist(knownCPPGram)

	# cppMaxGram = max(knownCPPHashFreq, key=knownCPPHashFreq.get)
	# print(cppMaxGram, knownCPPHashFreq[cppMaxGram])

###################################################################
# Section 2: Compare with known ngrams of code (Test Data)
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
# Section 3: to calculate trigram Probability
#############################################################################################
	kneserJava = nltk.KneserNeyProbDist(knownJavaHashFreq)
	kneserCPP = nltk.KneserNeyProbDist(knownCPPHashFreq)

	kneserJavaHash = convertProbListToHash(kneserJava)
	kneserCPPHash = convertProbListToHash(kneserCPP)
	 
	cpp = 0
	java = 0
	totalCppWithTag = 0
	totalJavaWithTag = 0
	totalJavaTags = 0
	totalCppTags = 0
	totalEval = 0

	resultsFile = open('Results.txt', 'a')
	codeFile = open('Code.txt', 'a')
	resultsFileString = codeFileString = ''

	# tree = ET.parse(xmldoc)
	# root = tree.getroot()
	for event, element in etree.iterparse(xmldoc, tag="row"):
		body = element.get('Body')
		# Only allow posts with a code tag to be added
		if '<code>' in body:
			postId = element.get('Id')
			# Tags for comment post
			tags = element.get('Tags')

			if tags == None:
				continue
			
			tags.lower()
			if not ('<java>' or '<c++>' or '<c++-faq>' or '<android>' or '<spring>' or '<swing>') in tags:
				continue

			code = parseBodyForTagCode(body)
			codeString = ''
			for item in code:
				snipetLength = len(item.split())
				if snipetLength > 3:
					codeString = codeString+re.sub('<code>|</code>',' ',item)
			
			codeString = re.sub('\n|\r|/\s\s+/g}',' ',codeString)
			codeString = re.sub('\.', ' ', codeString)
			codeString = re.sub('\t', '',codeString)
			codeString = re.sub(re.compile("/\*.*?\*/",re.DOTALL ) ,"" ,codeString)
			codeString = re.sub(re.compile("//.*?\n" ) ,"" ,codeString)
			codeString = re.sub( '[^0-9a-zA-Z]+', ' ', codeString )
			codeString = re.sub( '\s+', ' ', codeString).strip()

			codeFileString = codeFileString+codeString

			codeLength = len(codeString.split())
			# print(codeLength)
			if(codeLength < 3):
				continue

			totalEval += 1# total posts not skipped

			# In some cases a post can include tags associated with more than one languauge
			if ('<c++>' or '<c++-faq>') in tags:
				totalCppTags += 1
			if ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				totalJavaTags += 1

			# print(codeString)
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

			
			resultsFileString = resultsFileString+'Grams assigned as followed:\n'
			resultsFileString = resultsFileString+'PostId: {}\nC++: {} Java: {}\nCode: {} \n'.format(postId,cpp,java,codeString)
			if cpp > java:
				resultsFileString = resultsFileString+'Snippet determined to be C++\nTags include {}\n\n'.format(tags)
				if ('<c++>' or '<c++-faq>') in tags:
					totalCppWithTag += 1
			elif java > cpp:
				
				resultsFileString = resultsFileString+'Snippet determined to be Java\nTags include {}\n\n'.format(tags)
				if ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
					totalJavaWithTag += 1
			elif java == cpp:
				resultsFileString = resultsFileString+'Snippet determined to be inconclusive\nTags include {}\n\n'.format(tags)
			
			java = 0
			cpp = 0

			
			element.clear()
		for ancestor in element.xpath('ancestor-or-self::*'):
			while ancestor.getprevious() is not None:
				del ancestor.getparent()[0]


#############################################################################################
# Section Output
#############################################################################################

	resultsFile.write(resultsFileString)
	codeFile.write(codeFileString)

	print('Total Java snippets determined and also have tags (java, android, spring, swing): {}'.format(totalJavaWithTag))
	print('Total Java snippets: {}'.format(totalJavaTags))
	print('Total C++ snippets determined and also have tags (c++, c++-faq): {}'.format(totalCppWithTag))
	print('Total C++ snippets: {}'.format(totalCppTags))
	print('Total snippets evaluated: {}'.format(totalEval))
