"""
Part of Josiah-to-Annex Telnet code.
Determine number of notices printed.
"""

from __future__ import unicode_literals


class NumberDeterminer:



	foundFileName = ""
	noticesPrintedText = ""



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



	def figureNoticesNumber(self, screenText):

		# issue: key screenText substring can be *either* 'notices' or 'notice.

		import string

		returnVal = "init"

		# find position of ' notices printed.' text, *or* ' notice printed.' text.
		foundPosition = "init"
		noticesPosition = string.find( screenText, " notices printed." ) # haystack, needle. Will be -1 if not found
		noticePosition = string.find( screenText, " notice printed." ) # haystack, needle. Will be -1 if not found

		if(noticesPosition > -1):
			foundPosition = noticesPosition
		else:
			if(noticePosition > -1):
				foundPosition = noticePosition

		if(foundPosition != "init"):
			# backup 10 spaces (too much, but no problem), and create a 10-character segment.
			segment1start = foundPosition - 10
			segment1end = foundPosition
			segment1 = screenText[segment1start:segment1end]

			# find the start position of the text '[15;6H' and reduce the sement to start after the 'H'. This is our number.
			foundPosition2 = string.find(segment1, "[15;6H")

			if(foundPosition > -1):
				segment2start = foundPosition2 + 6
				segment2 = segment1[segment2start:]
				returnVal = segment2
				if( returnVal == "1" ):
					self.noticesPrintedText = "1 notice printed"
				else:
					self.noticesPrintedText = returnVal + " notices printed"
			else:
				returnVal = "noNumFound"

		else:
			returnVal = "noNumFound"

		return returnVal




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
