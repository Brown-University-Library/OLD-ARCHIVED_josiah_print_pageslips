"""
Part of LAS-to-Josiah code.
Obtain date in right format when needed.
"""


class DatePrepper:
		
		
		
	timeToFormat = ""
	


	def obtainDate(self):
		import time
		if( len(self.timeToFormat) == 0):
			theTime = time.localtime()
		else:
			theTime = self.timeToFormat
		formattedTime = time.strftime("%a %b %d %H:%M:%S %Z %Y", theTime)
		return formattedTime
		
		
		
	def prepareTimeStamp(self):
		import time
		if( len(self.timeToFormat) == 0):
			theTime = time.localtime()
		else:
			theTime = self.timeToFormat
		formattedTime = time.strftime("%Y-%m-%dT%H-%M-%S", theTime)
		return formattedTime
		
		
		
	def obtainOldDateInteger(self):
		"""Get the date integer representing one week ago"""
		
		import time
		dateNumberA = time.time()
		
		secondsInDay = (60*60*24)
		secondsInWeek = secondsInDay * 7
		
		dateNumberB = dateNumberA - secondsInWeek
		
		return dateNumberB
		
		
		
	def obtainMiniName(self):
		import string
		import time
		
		if( len(self.timeToFormat) == 0):
			rawDateInfo = time.localtime()
		else:
			rawDateInfo = self.timeToFormat
			
		month = time.strftime("%b", rawDateInfo)
		lowercaseMonth = string.lower(month)
		twoDigitDate = time.strftime("%d", rawDateInfo)
		
		hourAndMinute = time.strftime("%H%M", rawDateInfo)

		formattedTime = "jta_" + lowercaseMonth + twoDigitDate + "_" + hourAndMinute
		
		return formattedTime
	
	
	
	def obtainMiniNameTwo(self):
		import string
		import time
		
		if( len(self.timeToFormat) == 0):
			rawDateInfo = time.localtime()
		else:
			rawDateInfo = self.timeToFormat

		# <http://docs.python.org/lib/module-time.html> is your friend
		fourDigitYear = time.strftime("%Y", rawDateInfo)
		twoDigitMonth = time.strftime("%m", rawDateInfo)
		twoDigitDay = time.strftime("%d", rawDateInfo)
		twoDigitHour = time.strftime("%H", rawDateInfo)
		twoDigitMinute = time.strftime("%M", rawDateInfo)
		twoDigitSecond = time.strftime("%S", rawDateInfo)

		formattedTime = "jta_" + fourDigitYear + twoDigitMonth + twoDigitDay + "_" + twoDigitHour + twoDigitMinute + twoDigitSecond
		
		return formattedTime

		
		
# bottom