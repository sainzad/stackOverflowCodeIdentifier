# stackOverflowCodeIdentifier

Author: Andrew Sainz

How to use: To run from command line input "python XMLAnalyze.py Posts.xml KnownJava.txt KnownCpp.txt"

stackOverflowCodeIdentifier is designed to iterate through a collection of Post xml data collected from Stack Overflow forums. Data is then collected and each row tag is iterated through and evaluated. Use of the etree directory are utilized to traverse and get the element body of each row. Within each body contains code snippet indicated within the tag  . Snippet that contain greater than five words once parsed out, are then broken down into trigrams to be evaluated with the known languages corpus.

Once a list of trigrams is generated from the code snippet a frequency distribution will be created associated to each trigram. Use of the nltk.FreqDist() was utilized to calculate gram frequency. Using the frequency dictionary the process loops through each trigram. For each gram it will get the value from the pre determined known java and known c++ corpus. These values are then compared and determine if the snippet more reflexes java or c++. Once the process has made a selection on which language to select the element tag for the post row is searched. Examples of tags that are currently searched are .

Based from the knowledge gathered from the elements tag data the process will determine if it was correct in its selection or if it was incorrect. Statistical data is then gathered and used to determine overall results. The following are all formulas used to determine statistical data.

~~~~
javaSensitivity = presencePosJava / (presencePosJava+presenceNegJava) javaSpecificity = absenceNegJava / (absenceNegJava+absencePosJava) javaRateFalsePos = absencePosJava / (absencePosJava+absenceNegJava) javaRateFalseNeg = presenceNegJava / (presenceNegJava+presencePosJava) javaPosPredict = presencePosJava / (presencePosJava+ absencePosJava) javaNegPredict = presenceNegJava / (presenceNegJava+ absenceNegJava) javaRelativeRisk = (presencePosJava/ presencePosJava + presenceNegJava) / (absencePosJava / absencePosJava + absenceNegJava)

cppSensitivity = presencePosCpp / (presencePosCpp+presenceNegCpp) cppSpecificity = absenceNegCpp / (absenceNegCpp+absencePosCpp) cppRateFalsePos = absencePosCpp / (absencePosCpp+absenceNegCpp) cppRateFalseNeg = presenceNegCpp / (presenceNegCpp+presencePosCpp) cppPosPredict = presencePosCpp / (presencePosCpp+ absencePosCpp) cppNegPredict = presenceNegCpp / (presenceNegCpp+absenceNegCpp) cppRelativeRisk = (presencePosCpp/ presencePosCpp + presenceNegCpp) / (absencePosCpp / absencePosCpp + absenceNegCpp)
~~~~

# Files Used

- XMLAnalyze.py
	* Main program file and driving force for code identification and classification
- XMLParser.py
	* Contains parsing functions to extract each layer of xml tags to reach root of snippet code data.
- ngramFunctions.py
	* Contains functions for determining ngram data.
-frequencyFunctions.py
	* Contains functions for frequency calculations.
- CreateKnownCpp.py
	* Creates KnownCpp.txt file used in conjunction with the XMLAnalyze.py file.
- CreateKnownJava.py
	* Creates KnownJava.txt file used in conjunction with the XMLAnalyze.py file.
-Posts.xml
	* Posts.xml file contains all post data from Stack Overflow and is the key component for gathering snippet data.

#Files Created

-Analytics.txt
	*Output data providing overall calculations regarding the accuracy of code classification.
-Code.txt
	*Debug file that houses all code snippet data processed. 
-Results.txt
	*Debug output file outlining each post and it's associated code snippet data as well as how it was classified. 