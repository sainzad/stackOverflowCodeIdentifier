# Author: Andrew Sainz
# 
# Purpose: XMLAnalyze is designed to iterate through a collection of Post data collected from Stack Overflow
# 		   forums. Data collected to analyze the code tagged information to find the language of the code
# 		   being utilized.
# 
# How to use: To run from command line input "python XMLAnalyze.py Posts.xml"

import xml.etree.ElementTree as ET
import sys
import re
from nltk.util import ngrams

def parseBodyForTagCode(body):
	try:
		# Code is a string that contains all code tag data within the body
		# ex. code = ['<code>EXCEPT</code>, <code>LEFT JOIN</code>']
		code = [body[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', body)]
		# print(code)
	except AttributeError:
		code = None
	return code

def features(sentence):
	words = sentence.lower().split()
	return dict(('contains(%s)' %w, True) for w in words)

def createListOfCode(xmldoc):
	tree = ET.parse(xmldoc)
	root = tree.getroot()

	codeList = []

	for row in root:
	# Body holds all comment information from post
		body = row.get('Body')
		rowId = row.get('Id')
		# Tags for comment post
		tags = row.get('Tags')
		# parse body to find code tags
		code = parseBodyForTagCode(body)

		# Encode list information about code into UTF8
		codeUni = repr([x.encode('UTF8') for x in code])
		# If codes isn't present ignore post
		if codeUni == '[]':
			continue

		if tags != None:
			codeList.append(rowId+'`'+codeUni+'`'+tags)
		else:
			# unknown code tag is added to myList
			codeList.append(rowId+'`'+codeUni)
	return codeList

# Ngram section
############################################################################
def createNgramList(codeList,size):
	# Holds gramList for each item in codeList
	postGramList = []
	for item in codeList:
		allCodeTags = [item[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', item)]
		for code in allCodeTags:
			cleanCode = re.sub('<code>|</code>','',code)
			gramList = ngrams(cleanCode.split(), size)

		postGramList.append(gramList)
		
	return postGramList	

def calculateFrequency(c,d):
	return None

def ngramsFunction(input, n):
  input = input.split(' ')
  output = {}
  for i in range(len(input)-n+1):
    g = ' '.join(input[i:i+n])
    output.setdefault(g, 0)
    output[g] += 1
  return output

xmldoc = sys.argv[1]

myList = createListOfCode(xmldoc)
# print(myList)

gramList = createNgramList(myList,3)

test = ngramsFunction('This is a test of a test of a.',3)
print (test)

# print(gramList)
# for gram in gramList:
# 	postFreq = {}
# 	print('True')
# 	for snipets in gram:
# 		print(snipets)
		
			