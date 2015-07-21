# -*- coding: utf-8 -*-

"""
Part of Josiah-to-Annex Telnet code.
Determine number of notices printed.
"""

from __future__ import unicode_literals


class NumberDeterminer:



	foundFileName = ""
	noticesPrintedText = ""



	# def determineFileNumber(self, screenText):

	# 	# find fileName
	# 	# find position of fileName
	# 	# backup 5 positions
	# 	# capture next 3 characters
	# 	# remove possible trailing space
	# 	# remove possible preceeding 'H'
	# 	# what's left is our number

	# 	import re
	# 	import string

	# 	# find fileName

	# 	regexPattern = """
	# 		(jta_20)			# initial prefix
	# 		[0-9][0-9]		# rest of year
	# 		[0-9][0-9]		# month
	# 		[0-9][0-9]		# day
	# 		(_)				# separator
	# 		[0-9][0-9]		# hour
	# 		[0-9][0-9]		# minute
	# 		[0-9][0-9]		# second
	# 		(\.)(p)			# suffix
	# 		"""

	# 	searchResult = re.search(regexPattern, screenText, re.VERBOSE)

	# 	fileName = "init"
	# 	returnVal = "init"

	# 	if( searchResult == None):
	# 		returnVal = "-1"
	# 	else:
	# 		fileName = searchResult.group()
	# 		self.foundFileName = fileName

	# 	# find position of fileName and deduce fileName number

	# 	if( returnVal != "-1" ):
	# 		foundFileNamePosition = string.find( screenText, fileName )
	# 		numberStartPosition = foundFileNamePosition - 5
	# 		textSectionA = screenText[numberStartPosition:numberStartPosition+3]
	# 		textSectionB = string.strip(textSectionA)  # removes leading and trailing whitespace
	# 		if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
	# 			textSectionC = textSectionB[1:]
	# 		else:
	# 			textSectionC = textSectionB
	# 		returnVal = textSectionC

	# 	return returnVal




	def determineFileCount(self, screenText):

		# find pattern in screenText
		# store that number
		# delete all text up to and including this find.
		# look again.
		# if found, store number and repeat until no more finds occur.
		# at this point, the stored number is the count.

		import re
		import string

		# find pattern in screen text
		regexPattern = """
			(;1H)		# prefix
			[0-9]   	# targetNumber
			[ ][>][ ]	# suffix
			"""
		textToProcess = screenText
		highestNumber = 0
		loopFlag = "continue"
		while( loopFlag == "continue" ):
			searchResult = re.search(regexPattern, textToProcess, re.VERBOSE)
			if( searchResult == None):
				break
			else:
				foundText = searchResult.group()
				#store the number
				highestNumber = foundText[3:4]
				# delete all text up to and including this find.
				foundTextStartPosition = string.find( textToProcess, foundText ) # haystack, needle. Will be -1 if not found
				foundTextLength = len(foundText)
				textToProcess = textToProcess[foundTextStartPosition + foundTextLength:]

		# at this point, the stored number is the count
		returnVal = int(highestNumber)
		return returnVal



# bottom
