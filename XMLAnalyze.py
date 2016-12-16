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
from random import randint
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
	knownJava = sys.argv[2]
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
	
#############################################################################################
# Section 2: to calculate trigram Probability
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
	analyticsFile = open('Analytics.txt', 'a')

	resultsFileString = codeFileString = analyticsString = ''

	presencePosCpp = presenceNegCpp = absencePosCpp = absenceNegCpp =0
	presencePosJava = presenceNegJava = absencePosJava = absenceNegJava = 0

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
			# if not ('<java>' or 'c++' or '<c>' or '<c++-faq>' or '<android>' or '<spring>' or '<swing>' or '<pass-by-reference>' or '<eclipse>' or '<regex>' or '<recursion>' or '<binary-tree>' or '<software-engineering>' or '<divide-by-zero>' or '<arraylist>' or '<garbage-collection>' or '<object>' or '<arrays>' or '<iterator>' or '<hashcode>' or '<inheritance>' or '<tostring>' or '<unicode>' or '<quicksort>' or '<sorting>' or '<jar>' or '<bubble-sort>' or '<hashcode>' or '<multidimensional-array>' or '<codebase>' or '<class>') in tags:
			# 	continue

			# Skip if post contains tags from multiple languauges
			# if (('<c++>' or '<c++-faq>' or '<c>' in tags) and ('<java>' or '<android>' or '<spring>' or '<swing>' in tags)) :
			# 	continue

			code = parseBodyForTagCode(body)
			codeString = ''
			for item in code:
				snipetLength = len(item.split())
				if snipetLength > 5:
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
			if ('c++' or '<c++-faq>' or '<c>') in tags:
				totalCppTags += 1
			if ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				totalJavaTags += 1

			# print(codeString)
			codeList = ngrams(codeString.split(' '),5)
			codeGram = nltk.FreqDist(codeList)
			

			for gram in codeGram:
				cppValue = kneserCPPHash.get(str(gram))
				javaValue = kneserJavaHash.get(str(gram))


				if cppValue != None and javaValue != None:
					# Compare to the frequency values
					if cppValue > javaValue:
						cpp += 1
					else:
						java += 1
				# if there is a hit for either one then add to hit value
				elif cppValue == None and javaValue != None:
					java += 1
				elif cppValue != None and javaValue == None:
					cpp += 1
			
			# if hit values are the same make a guess on language
			if java == cpp:
				ran  = randint(0,1)
				if(ran == 0):
					java += 1
				else:
					cpp += 1

			# Done looking for gram hit values
			#################################
			# fix absence
			#################################
			# if java == 0 and ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
			# 	absenceNegJava += 1
			# if cpp == 0 and ('c++' or '<c++-faq>' or '<c>') in tags:
			# 	absenceNegCpp += 1
			# if java > cpp and not ('java' or '<android>' or '<spring>' or '<swing>')  in tags:
			# 	print('absence is true')
			# 	absencePosJava += 1
			# if cpp > java and not ('c++' or '<c++-faq>' or '<c>') in tags:
			# 	absencePosCpp += 1
			#################################
			# if no values where hit then move on to next post row
			# if java == 0 and cpp == 0:
			# 	continue
			
			determinedCpp = determinedJava = False

			resultsFileString = resultsFileString+'Grams assigned as followed:\n'
			resultsFileString = resultsFileString+'PostId: {}\nC++: {} Java: {}\nCode: {} \n'.format(postId,cpp,java,codeString)
			if cpp > java:
				resultsFileString = resultsFileString+'Snippet determined to be C++\nTags include {}\n\n'.format(tags)
				determinedCpp = True
				# if ('c++' or '<c++-faq>' or '<c>') in tags:
				# 	totalCppWithTag += 1
			elif java > cpp:
				resultsFileString = resultsFileString+'Snippet determined to be Java\nTags include {}\n\n'.format(tags)
				determinedJava = True
				# if ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				# 	totalJavaWithTag += 1
			
			# analyze results
			
			if determinedCpp == True and ('c++' or '<c++-faq>' or '<c>') in tags:
				presencePosCpp += 1
			if determinedCpp == False and ('c++' or '<c++-faq>' or '<c>') in tags:
				presenceNegCpp += 1
			if determinedCpp == True and not('c++' or '<c++-faq>' or '<c>') in tags:
				absencePosCpp += 1
			if determinedCpp == False and not('c++' or '<c++-faq>' or '<c>') in tags:
				absenceNegCpp += 1

			if determinedJava == True and ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				presencePosJava += 1
			if determinedJava == False and ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				presenceNegJava += 1
			if determinedJava == True and not('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				absencePosJava += 1
			if determinedJava == False and not('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
				absenceNegJava += 1


			# if ('c++' or '<c++-faq>' or '<c>') in tags:
			# 	# presence is true
			# 	if cpp > java:
			# 		# positive is true
			# 		# true positive
			# 		presencePosCpp += 1
			# 	else:
			# 		# false negative
			# 		presenceNegCpp += 1
			# # elif cpp > java:
			# # 	# been determined cpp but no cpp tags
			# # 	# incorectly determined
			# # 	# false positive
			# # 	absencePosCpp += 1
			# # else:
			# # 	# determined not to be cpp correctly
			# # 	# true negative
			# # 	absenceNegCpp += 1
			
			# if ('<java>' or '<android>' or '<spring>' or '<swing>') in tags:
			# 	# presence is true
			# 	if java > cpp:
			# 		presencePosJava += 1
			# 	else:
			# 		presenceNegJava += 1
			# # elif java > cpp:
			# 	absencePosJava += 1
			# else: 
			# 	absenceNegJava += 1

			java = 0
			cpp = 0

			
			element.clear()  
		for ancestor in element.xpath('ancestor-or-self::*'):
			while ancestor.getprevious() is not None:
				del ancestor.getparent()[0]


	
	javaSensitivity = presencePosJava / (presencePosJava+presenceNegJava)
	javaSpecificity = absenceNegJava / (absenceNegJava+absencePosJava)
	javaRateFalsePos = absencePosJava / (absencePosJava+absenceNegJava)
	javaRateFalseNeg = presenceNegJava / (presenceNegJava+presencePosJava)
	javaPosPredict = presencePosJava / (presencePosJava+ absencePosJava)
	javaNegPredict = presenceNegJava / (presenceNegJava+ absenceNegJava)
	javaRelativeRisk = (presencePosJava/ (presencePosJava + presenceNegJava)) / (absencePosJava / (absencePosJava + absenceNegJava))
	
	cppSensitivity = presencePosCpp / (presencePosCpp+presenceNegCpp)
	cppSpecificity = absenceNegCpp / (absenceNegCpp+absencePosCpp)
	cppRateFalsePos = absencePosCpp / (absencePosCpp+absenceNegCpp)
	cppRateFalseNeg = presenceNegCpp / (presenceNegCpp+presencePosCpp)
	cppPosPredict = presencePosCpp / (presencePosCpp+ absencePosCpp)
	cppNegPredict = presenceNegCpp / (presenceNegCpp+absenceNegCpp)
	cppRelativeRisk = (presencePosCpp/ (presencePosCpp + presenceNegCpp)) / (absencePosCpp / (absencePosCpp + absenceNegCpp))

	analyticsString = 'Java\n------\nTrue Positive: {}\nFalse Negative: {}\nFalse Positive: {}\nTrue Negative: {}'.format(presencePosJava,presenceNegJava,absencePosJava,absenceNegJava)
	analyticsString += '\nSensitivity: {}\nSpecificity: {}'.format(javaSensitivity, javaSpecificity)
	analyticsString += '\nRate False Positives: {}\nRate False Negatives: {}'.format(javaRateFalsePos, javaRateFalseNeg)
	analyticsString += '\nEstimate Positive Predictive Value: {}\nEstimate Negative Predictive Value: {}'.format(javaPosPredict, javaNegPredict)
	analyticsString += '\nRelative Risk: {}'.format(javaRelativeRisk)

	analyticsString += '\n\nC++\n------\nTrue Positive: {}\nFalse Negative: {}\nFalse Positive: {}\nTrue Negative: {}'.format(presencePosCpp,presenceNegCpp,absencePosCpp,absenceNegCpp)
	analyticsString += '\nSensitivity: {}\nSpecificity: {}'.format(cppSensitivity, cppSpecificity)
	analyticsString += '\nRate False Positives: {}\nRate False Negatives: {}'.format(cppRateFalsePos, cppRateFalseNeg)
	analyticsString += '\nEstimate Positive Predictive Value: {}\nEstimate Negative Predictive Value: {}'.format(cppPosPredict, cppNegPredict)
	analyticsString += '\nRelative Risk: {}'.format(cppRelativeRisk)


#############################################################################################
# Section Output
#############################################################################################

	resultsFile.write(resultsFileString)
	codeFile.write(codeFileString)
	analyticsFile.write(analyticsString)

	# print('Total Java snippets determined and also have tags (java, android, spring, swing): {}'.format(totalJavaWithTag))
	# print('Total Java snippets: {}'.format(totalJavaTags))
	# print('Total C++ snippets determined and also have tags (c++, c++-faq, c): {}'.format(totalCppWithTag))
	# print('Total C++ snippets: {}'.format(totalCppTags))
	# print('Total snippets evaluated: {}'.format(totalEval))