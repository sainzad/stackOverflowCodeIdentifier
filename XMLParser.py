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
		code = None
	return code

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

def gatherKnownTags(givenList, searchLanguage):
	knownList = []

	for entry in givenList:
		try:
			print(searchLanguage.lower())
			print(searchLanguage.lower() in entry.lower())
			if searchLanguage.lower() in entry.lower():
				knownList.append(entry)
		except:
			# Pass if there were no tags in the entry
			pass
	return knownList