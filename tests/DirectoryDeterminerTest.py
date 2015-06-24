"""
DirectoryDeterminerTest.py
"""


import DirectoryDeterminer
import unittest



class DirectoryDeterminerTest(unittest.TestCase):



	def testDetermineEnclosingDirectory(self):
		determinerInstance = DirectoryDeterminer.DirectoryDeterminer()
		path = "zz"
   		expected = "zz"
   		result = determinerInstance.determineEnclosingDirectory(path)
		self.assertEqual( expected, result, "result is: " + str(result) )



	def testDetermineRunningScript(self):
		import sys
		determinerInstance = DirectoryDeterminer.DirectoryDeterminer()
		returnedVal = determinerInstance.determineRunningScript( sys.argv[0] )
		possibleVal_a = "DirectoryDeterminerTest.py"
		possibleVal_b = "_regression.py"  # when all tests are run
		expected = True
		result = (returnedVal == possibleVal_a) or (returnedVal == possibleVal_b)
		self.assertEqual( expected, result, "result is: " + str(result) )



if __name__ == "__main__":
	unittest.main()



# bottom
