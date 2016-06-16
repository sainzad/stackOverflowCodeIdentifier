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

def parseBodyForTagCode(body):
	try:
		# Code is a string that contains all code tag data within the body
		# ex. code = ['<code>EXCEPT</code>, <code>LEFT JOIN</code>']
		code = [body[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', body)]
		# print(code)
	except AttributeError:
		code = ''
	return code

xmldoc = sys.argv[1]

tree = ET.parse(xmldoc)
root = tree.getroot()

# print (root.attrib)

# for each row in the xml document gather body information
for row in root:
	# Body holds all comment information from post
	body = row.get('Body')
	# parse body to find code tags
	code = parseBodyForTagCode(body)
	# Encode list information about code into UTF8
	codeUni = repr([x.encode('UTF8') for x in code])

	print (codeUni)
	