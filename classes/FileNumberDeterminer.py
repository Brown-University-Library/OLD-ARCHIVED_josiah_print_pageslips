# -*- coding: utf-8 -*-

"""
Part of Josiah-to-Annex Telnet code.
Determine number of notices printed.
"""

from __future__ import unicode_literals


class FileNumberDeterminer:



	foundFileName = ""



#	def determineFileNumber(self, screenText):
#
#		# find position of fileName
#		# backup 5 positions
#		# capture next 3 characters
#		# remove possible trailing space
#		# remove possible preceeding 'H'
#		# what's left is our number
#
#		import string
#
#		returnVal = "init"
#		lengthCheck = "init"
#
#		fileIdentifier = "jta_2006"
#		foundPosition = string.find( screenText, fileIdentifier ) # haystack, needle. Will be -1 if not found
#
#		# let's check the file info just to be SURE
#
#		if(foundPosition != -1):
#			self.foundFileName = screenText[foundPosition:foundPosition + 21]
#
#			startPosition = foundPosition - 5
#			textSectionA = screenText[startPosition:startPosition+3]
#			textSectionB = string.strip(textSectionA) # removes leading and trailing whitespace
#			if(textSectionB[0:1] == 'H'):
#				textSectionC = textSectionB[1:]
#			else:
#				textSectionC = textSectionB
#			returnVal = textSectionC
#		else:
#			returnVal = "-1"
#
#		return returnVal



	def determineFileNumber(self, screenText):

		# find fileName
		# find position of fileName
		# backup 5 positions
		# capture next 3 characters
		# remove possible trailing space
		# remove possible preceeding 'H'
		# what's left is our number

		import re
		import string

		# find fileName

		regexPattern = """
			(jta_20)			# initial prefix
			[0-9][0-9]		# rest of year
			[0-9][0-9]		# month
			[0-9][0-9]		# day
			(_)				# separator
			[0-9][0-9]		# hour
			[0-9][0-9]		# minute
			[0-9][0-9]		# second
			(\.)(p)			# suffix
			"""

		searchResult = re.search(regexPattern, screenText, re.VERBOSE)

		fileName = "init"
		returnVal = "init"

		if( searchResult == None):
			returnVal = "-1"
		else:
			fileName = searchResult.group()
			self.foundFileName = fileName

		# find position of fileName and deduce fileName number

		if( returnVal != "-1" ):
			foundFileNamePosition = string.find( screenText, fileName )
			numberStartPosition = foundFileNamePosition - 5
			textSectionA = screenText[numberStartPosition:numberStartPosition+3]
			textSectionB = string.strip(textSectionA)  # removes leading and trailing whitespace
			if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
				textSectionC = textSectionB[1:]
			else:
				textSectionC = textSectionB
			returnVal = textSectionC

		return returnVal



	def validateName(self, fileName):

		import re

		validationResult = "init"
#		properLength = 21
#
#		# check length
#		fileNameLength = len(fileName)
#		if( fileNameLength != properLength ):
#			validationResult = "failure - length should be " + str(properLength) + " but is " + str(fileNameLength)

		# check format
		pattern = """
			(jta_20)			# initial prefix
			[0-9][0-9]		# rest of year
			[0-9][0-9]		# month
			[0-9][0-9]		# day
			(_)				# separator
			[0-9][0-9]		# hour
			[0-9][0-9]		# minute
			[0-9][0-9]		# second
			(\.)(p)			# suffix
			"""
		if( re.search(pattern, fileName, re.VERBOSE) == None ):
			validationResult = "failure - improper format"

		# checks done
		if( validationResult == "init" ):
			validationResult = "ok"

		return validationResult


#	def determineFileNumber(self, screenText, fileName):
#
#		# find position of fileName
#		# backup 5 positions
#		# capture next 3 characters
#		# remove possible trailing space
#		# remove possible preceeding 'H'
#		# what's left is our number
#
#		import string
#
#		returnVal = "init"
#
#		foundPosition = string.find( screenText, fileName ) # haystack, needle. Will be -1 if not found
#
#		if(foundPosition != -1):
#			startPosition = foundPosition - 5
#			textSectionA = screenText[startPosition:startPosition+3]
#			textSectionB = string.strip(textSectionA) # removes leading and trailing whitespace
#			if(textSectionB[0:1] == 'H'):
#				textSectionC = textSectionB[1:]
#			else:
#				textSectionC = textSectionB
#			returnVal = textSectionC
#		else:
#			returnVal = -1
#
#		return returnVal



# bottom
