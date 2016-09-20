import sys
import re
from nltk.util import ngrams

def calculateFrequency(knownFreq,unknownFreq):
	return knownFreq/unknownFreq

def convertProbListToHash(inList):
	outHash = {}

	for i in inList.samples():
		key = str(i) # Converts Tuple to string
		value = inList.prob(i)
		outHash.update({key:value})

	return outHash