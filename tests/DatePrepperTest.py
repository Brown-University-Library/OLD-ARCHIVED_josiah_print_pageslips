"""
Part of LAS-to-Josiah code.
"""

from __future__ import unicode_literals

import unittest
from josiah_print_pageslips.classes import DatePrepper


class DatePrepperTest(unittest.TestCase):



	def testPrepDate_sentTime(self):
		"""sending a known time to check formatting"""
		datePrepperInstance = DatePrepper.DatePrepper()
		datePrepperInstance.timeToFormat = (2005, 7, 13, 13, 41, 39, 2, 194, 1) # 'Wed Jul 13 13:41:39 EDT 2005'
		expected = "Wed Jul 13 13:41:39 EDT 2005"
		result = datePrepperInstance.obtainDate()
		self.assertEqual(expected, result, "result is: " + str(result))



	def testPrepDate_sentTime(self):
		"""ensuring that no sent time still returns a string""" # I *could* check that what's returned is a legit time, but noooo.
		datePrepperInstance = DatePrepper.DatePrepper()
		returnedTime = datePrepperInstance.obtainDate()
		expected = len("abc") > 1
		result = len(returnedTime) > 1
		self.assertEqual(expected, result, "result is: " + str(result))



	def testObtainMiniNameTwo_withSentDate(self):
		"""create name for page-slip save"""

		datePrepperInstance = DatePrepper.DatePrepper()
		datePrepperInstance.timeToFormat = (2005, 8, 2, 9, 5, 39, 2, 194, 1) # 'Wed Aug 2 09:05:39 EDT 2005'

		expected = "jta_20050802_090539"
		result = datePrepperInstance.obtainMiniNameTwo()
		self.assertEqual( expected, result, "result is: " + str(result) )



if __name__ == "__main__":
	unittest.main()



# bottom
