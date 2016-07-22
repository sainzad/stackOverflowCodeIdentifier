import unittest
from XMLAnalyze import *

class TestStringMethods(unittest.TestCase):
    
    def test_listOfCode(self):
        xmldoc = 'Posts2.xml'
        self.assertTrue(createListOfCode(xmldoc),None)

    def test_isIN(self):
        xmldoc = 'Posts2.xml'
        myList = createListOfCode(xmldoc)
        self.assertTrue(gatherKnownTags(myList, 'java'))

    def test_listOfCodeSample(self):
        xmldoc = 'PostsSample.xml'
        self.assertTrue(createListOfCode(xmldoc),None)

if __name__ == '__main__':
    unittest.main()