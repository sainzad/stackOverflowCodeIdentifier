# Author: Andrew Sainz
# 
# Purpose: XMLParser is designed to iterate through a collection of Post data collected from Stack Overflow
# 		   forums. Data collected to analize the code tagged information to find the language of the code
# 		   being utilized.
# 
# How to use: To run from command line input "python XMLParser.py [XML file name].xml"

import xml.etree.ElementTree as ET
import sys
import re
from nltk.util import ngrams
from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.classify import PositiveNaiveBayesClassifier

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

# Known list tag fields
knownJavaTags = []
knownJavaMention = []
knownC = []
knownCSharp = []
knownPython = []


xmldoc = sys.argv[1]

tree = ET.parse(xmldoc)
root = tree.getroot()

# print (root.attrib)
myList = []
# for each row in the xml document gather body information
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
	# If code isn't present ignore post move to next post
	if codeUni == '[]':
		continue

	cleanCode = ""
	for element in codeUni:
		print (element is str)
		element.decode()
		cleanCode = element + cleanCode
	cleanCode = re.sub('<code>|</code>','',cleanCode)
	print (cleanCode)

	if tags != None:
		# Assign all known code to list
		if ("<java>" in tags):
			knownJavaTags.append(codeUni)
		if ("<python>" in tags) or ("python" in body):
			knownPython.append(rowId+'`'+codeUni+'`'+tags)
		if ("<C>" in tags) or ("C" in body):
			knownC.append(rowId+'`'+codeUni+'`'+tags)
		if ("<C#>" in tags) or ("C#" in body):
			knownCSharp.append(rowId+'`'+codeUni+'`'+tags)
		# Known post tags are added to myList
		myList.append(rowId+'`'+codeUni+'`'+tags)
	else:
		# unknown code tag is added to myList
		myList.append(rowId+'`'+codeUni)

	if "java" in body:
			knownJavaMention.append(codeUni)

# Assign positive features
positive_featuresets = list(map(features, knownJavaTags))
unlabeled_featuresets = list(map(features, knownJavaMention))
classifier = PositiveNaiveBayesClassifier.train(positive_featuresets, unlabeled_featuresets)


# Ngram section
# print(myList)

############################################################################
for item in myList:
	allCodeTags = [item[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', item)]
	for code in allCodeTags:
		cleanCode = re.sub('<code>|</code>','',code)
		# print (cleanCode)
		# print(classifier.classify(features(cleanCode)))
		trigrams = ngrams(cleanCode.split(), 3)
		# for grams in trigrams:
	  		# print (grams)
	# break	