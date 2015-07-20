"""
Part of Josiah-to-Annex Telnet code.
Manage screen navigation.
"""

from __future__ import unicode_literals

import unittest
from josiah_print_pageslips.classes import Emailer


class EmailerTest(unittest.TestCase):



	def testSendEmail_goodDataSoNoErrors(self):
		"""sending email"""

		emailerInstance = Emailer.Emailer()
		message = "test message"

		expected = "success"
		result = emailerInstance.sendEmail(message)
		self.assertEqual(expected, result, "result is: " + str(result))




	def testImportEmailPrefs_recipient(self):
		"""test that recipients attribute is correct"""

		emailerInstance = Emailer.Emailer()
#		message = "test message"

		expected = ['zz'] #
		result = emailerInstance.recipientList
		self.assertEqual(expected, result, "result is: " + str(result))



	def testImportEmailPrefs_headerTo(self):
		"""test that toHeader attribute is correct"""

		emailerInstance = Emailer.Emailer()
#		message = "test message"

		expected = "To: zz"
		result = emailerInstance.headerTo
		self.assertEqual(expected, result, "result is: " + str(result))



if __name__ == "__main__":
	unittest.main()



# bottom
