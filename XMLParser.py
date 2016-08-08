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

def createHash(xmldoc,comments):
	tree = ET.parse(xmldoc)
	root = tree.getroot()

	myHash = {}
	myHashOut = {}

	for row in root:
		body = row.get('Body')
		postId = row.get('Id')
		# Tags for comment post
		tags = row.get('Tags')	
		
		if tags != None:
			value = body+'`'+tags
			myHash.update({postId:value})
			# myList.append(rowId+'`'+body+'`'+tags)
		else:
			# unknown code tag is added to myList
			myHash.update({postId:body})
			# myList.append(rowId+'`'+body)

	myHashOut = addCommentsToHash(myHash,comments)
	# print(len(myHash))
	return myHashOut

def addCommentsToHash(myHash,comments):
	commentTree = ET.parse(comments)
	commentRoot = commentTree.getroot()
	myHashCom = {}

	for row in commentRoot:
		parentPostId = row.get('PostId')
		commentBody = row.get('Text')
		hashValue = myHash.get(parentPostId)
		# If post key can be found add comment information to value
		try:
			myHash.put({parentPostId:hashValue+'`'+commentBody})
		except:
			pass

	myHashCom = myHash
	return myHashCom

def gatherKnown(givenHash, searchTerms):
	knownHash = {}

	for key,value in givenHash.items():
		# print(searchLanguage.lower())
		# print(searchLanguage.lower() in entry.lower())
		for term in searchTerms:
			if term.lower() in value.lower():
				knownHash.update({key:value})
	return knownHash