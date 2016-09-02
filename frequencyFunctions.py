import sys
import re

def calculateFrequency(size,value):
	return value/size

def createFrequencyHash(gramHash):
	freqHash = {}
	gramHashSize = len(gramHash)

	for key in gramHash.keys():
		gramValue = gramHash[key]
		freq = calculateFrequency(gramHashSize,gramValue)
		freqHash.update({key:freq})

	return freqHash

def ngramProbability(knownHash, dataHash, dataHashKey):
	prob = 0
	knownValue = knownHash.get(dataHashKey);
	dataHashValue = dataHash.get(dataHashKey);

	try:
		prob = dataHashValue/knownValue
	except:
		prob = -999

	return prob