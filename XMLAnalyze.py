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

def parseBodyForTagCode(body):
	try:
		# Code is a string that contains all code tag data within the body
		# ex. code = ['<code>EXCEPT</code>, <code>LEFT JOIN</code>']
		code = [body[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', body)]
		# print(code)
	except AttributeError:
		code = None
	return code

# Known list tag fields
knownJava = []
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
		
	# If code isn't present ignore
	if codeUni == '[]':
		continue
	# print (codeUni)
	if tags != None:
		# Assign all known code to list
		if ("<java>" in tags) or ("java" in body):
			knownJava.append(rowId+'`'+codeUni+'`'+tags)
		if ("<python>" in tags) or ("python" in body):
			knownPython.append(rowId+'`'+codeUni+'`'+tags)
		if ("<C>" in tags) or ("C" in body):
			knownC.append(rowId+'`'+codeUni+'`'+tags)
		if ("<C#>" in tags) or ("C#" in body):
			knownCSharp.append(rowId+'`'+codeUni+'`'+tags)
		myList.append(rowId+'`'+codeUni+'`'+tags)
	else:
		myList.append(rowId+'`'+codeUni)


# Ngram section
# print(myList)

############################################################################
for item in myList:
	allCodeTags = [item[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', item)]
	for code in allCodeTags:
		cleanCode = re.sub('<code>|</code>','',code)
		# print (cleanCode)
		trigrams = ngrams(cleanCode.split(), 3)
		for grams in trigrams:
	  		print (grams)
	# break	