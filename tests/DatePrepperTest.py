"""
Part of LAS-to-Josiah code.
"""

from __future__ import unicode_literals

import DatePrepper
import unittest



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



	def testPrepareTimeStamp_checkKnownTime(self):
		"""sending a known time to check formatting"""
		datePrepperInstance = DatePrepper.DatePrepper()
		datePrepperInstance.timeToFormat = (2005, 7, 13, 13, 41, 39, 2, 194, 1) # 'Wed Jul 13 13:41:39 EDT 2005'
		expected = "2005-07-13T13-41-39"
		result = datePrepperInstance.prepareTimeStamp()
		self.assertEqual(expected, result, "result is: " + str(result))



	def testObtainOldFileInteger(self):
		"""Test getting the date integer representing one week ago"""

		import time
		currentDateInteger = time.time()

		datePrepperInstance = DatePrepper.DatePrepper()
		oldDateInteger = datePrepperInstance.obtainOldDateInteger()

		secondsInDay = (60*60*24)
		secondsInWeek = secondsInDay * 7
		comparisonDateInteger = oldDateInteger + secondsInWeek

		expected = True
		result = (comparisonDateInteger - currentDateInteger) < 5 # not a great check; manually redoes the function and makes sure the two numbers aren't more than five seconds apart
		self.assertEqual(expected, result, "result is: " + str(result))



	def testObtainMiniName_withSentDate(self):
		"""create name for page-slip save"""

		datePrepperInstance = DatePrepper.DatePrepper()

		datePrepperInstance.timeToFormat = (2005, 8, 2, 9, 5, 39, 2, 194, 1) # 'Wed Aug 2 09:05:39 EDT 2005'

		expected = "jta_aug02_0905"
		result = datePrepperInstance.obtainMiniName()
		self.assertEqual( expected, result, "result is: " + str(result) )



	def testObtainMiniName_withNoSentDate(self):
		"""create name for page-slip save"""

		datePrepperInstance = DatePrepper.DatePrepper()
		returnedTime = datePrepperInstance.obtainMiniName()

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
