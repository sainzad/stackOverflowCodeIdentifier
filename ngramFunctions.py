import sys
import re

def createNgramHash(inputHash,size):
	# Holds gramList for each item in codeList
	postGramHash = {}
	for key,value in inputHash.items():
		allCodeTags = [value[m.start():m.end()] for m in re.finditer('<code>(.+?)</code>', value)]
		for code in allCodeTags:
			cleanCode = re.sub('<code>|</code>','',code)
			# gramList = ngrams(cleanCode.split(), size)
			postGramHash.update(ngramsFunction(cleanCode, 3))
		
	return postGramHash	

def ngramsFunction(input, n):
	input = input.split(' ')
	output = {}
	for i in range(len(input)-n+1):
	    g = ' '.join(input[i:i+n])
	    output.setdefault(g, 0)
	    output[g] += 1

	return output
