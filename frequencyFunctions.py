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