# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys, unittest
from josiah_print_pageslips.classes import DirectoryDeterminer


class DirectoryDeterminerTest( unittest.TestCase ):

	def testDetermineEnclosingDirectory(self):
		determinerInstance = DirectoryDeterminer.DirectoryDeterminer()
		path = 'zz'
   		expected = 'zz'
   		result = determinerInstance.determineEnclosingDirectory(path)
		self.assertEqual( expected, result, "result is: " + str(result) )

	def testDetermineRunningScript(self):
		determinerInstance = DirectoryDeterminer.DirectoryDeterminer()
		returnedVal = determinerInstance.determineRunningScript( sys.argv[0] )
		possibleVal_a = 'DirectoryDeterminerTest.py'
		possibleVal_b = '_regression.py'  # when all tests are run
		expected = True
		result = (returnedVal == possibleVal_a) or (returnedVal == possibleVal_b)
		self.assertEqual( expected, result, "result is: " + str(result) )


if __name__ == '__main__':
	unittest.main()
