# top


'''
Part of Josiah-to-Annex Telnet code.
Manage export of Annex requests to Annex server.
'''



class FileTransferController:



	log = ""
	debug = "off"  # "on", "off"



	def runCode(self):

		#######
		# setup environment
		#######

		import os
		import sys

		try:
			os.chdir("zz")  # worf: to handle production server cron call
		except:
			pass
		mainDirectoryPath = os.path.abspath('')

		newLogEntry = "mainDirectoryPath: " + str(mainDirectoryPath)
		if(self.debug == "on"):
			print "debug starts"  # for live step-by-step output
			self.log = self.log + "\n" + "debug starts"  # to also include in actual log
#			self.log = self.log + "\n" + newLogEntry
#			print newLogEntry

		sys.path.append(mainDirectoryPath + '/libraries/pexpect-2.0/')
		sys.path.append(mainDirectoryPath + '/classes/')

#		newLogEntry = "updated sys.path: " + str(sys.path)
#		if(self.debug == "on"):
#			self.log = self.log + "\n" + newLogEntry
#			print newLogEntry

		import DirectoryDeterminer # to get reference to enclosing folder for import of PrivatePrefs
		ddInstance = DirectoryDeterminer.DirectoryDeterminer()
		enclosingDirectoryPath = ddInstance.determineEnclosingDirectory(mainDirectoryPath)
		sys.path.append(enclosingDirectoryPath)

		import pexpect
		import DatePrepper
		import NumberDeterminer
		import Prefs # Prefs constructor loads PrivatePrefs

		# now that I have a reference to DatePrepper, I can set up the log heading
		datePrepperInstance = DatePrepper.DatePrepper()
		dateAndTimeText = datePrepperInstance.obtainDate()
		self.log = "Automated ssh session starting at " + dateAndTimeText + "\n" + self.log
		self.log = "\n" + "-------" + "\n\n" + self.log

		newLogEntry = "setup complete"
		if(self.debug == "on"):
			self.log = self.log + "\n" + newLogEntry
			print newLogEntry



		#######
		# load preferences
		#######

		prefsInstance = Prefs.Prefs()
		sshTargetHost = prefsInstance.sshTargetHost
		loginName = prefsInstance.loginName
		loginPassword = prefsInstance.loginPassword
		initialsName = prefsInstance.initialsName
		initialsPassword = prefsInstance.initialsPassword

		newLogEntry = "prefs loaded"
		if(self.debug == "on"):
			self.log = self.log + "\n" + newLogEntry
			print newLogEntry



		#######
		# connect
		#######

		try:
			child = pexpect.spawn('ssh ' + loginName + "@" + sshTargetHost)
			if(self.debug == "on"):
				child.logfile = sys.stdout
			child.delaybeforesend = .5
		except:
			newLogEntry = "connect via ssh FAILED"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		newLogEntry = "connect via ssh step - success"
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry




		#######
		# authenticate
		#######

		try:
			child.expect('password: ')
			child.sendline( loginPassword )
		except:
			newLogEntry = "Login step FAILED"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		newLogEntry = 'login step - success'
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# access *** MAIN MENU ***
		#######

		screenNameText = "access 'Main menu' screen step - "
		try:
			child.expect('Choose one')  # "Choose one (S,D,C,M,A,Q)"
			newLogEntry = screenNameText + "success"
		except:
			newLogEntry = screenNameText + "FAILURE"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# access 'Additional system functions' screen
		#######

		screenNameText = "access 'Additional system functions' screen step - "
		try:
			child.send('A')  # "A > ADDITIONAL system functions"
			child.expect("key your initials")
			child.sendline(initialsName)
			child.expect("key your password")
			child.sendline(initialsPassword)
			child.expect("ADDITIONAL SYSTEM FUNCTIONS")
			child.expect("Choose one")  # "Choose one (C,B,S,M,D,R,E,V,F,N,U,O,A,Q)"
		except:
			newLogEntry = screenNameText + "FAILURE"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		newLogEntry = screenNameText + "success"
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# access 'Read/write MARC records' screen
		#######

		screenNameText = "access 'Read/write marc records' screen step - "
		try:
			child.send('M')  # "M > Read/write MARC records"
			child.expect("READ/WRITE MARC RECORDS")
			child.expect("Choose one")  # "Choose one (B,A,S,N,P,X,U,M,L,F,T,Q)"
		except:
			newLogEntry = screenNameText + "FAILURE"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		newLogEntry = screenNameText + "success"
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# access 'Send print files out of innopac' screen
		#######

		screenNameText = "access 'Send print files out of innopac' screen step - "
		try:
			child.send('F')  # "F > Send print files out of INNOPAC using FTP"
			child.expect("Send print files out of INNOPAC")
			option = child.expect(["Choose one", "until their combined total size"])  # "Choose one (F,R,Y,Q)"
		except:
			newLogEntry = screenNameText + "FAILURE"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		if(option == 0):
			newLogEntry = screenNameText + "success"
		if(option == 1):
			newLogEntry = screenNameText + "FAILURE: PROBLEM: total size of files in FTP list is too big"
			newLogEntry = newLogEntry + "\n" + "closing session"
			if(self.debug == "on"):
				print newLogEntry
			self.endProgram(newLogEntry, "problem", child)

		# if I get here all was well
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# Build list of files
		# If no JTAs, exit
		# If a JTA exists, remember it -> try to send it -> delete it (basically continue)
		#######



		#######
		# access 'Innopac file transfer' screen
		# Look for file to send
		#######

		screenNameText = "access 'Innopac file transfer' screen step - "

		fnDeterminerInstance = NumberDeterminer.NumberDeterminer()
		textToExamine = child.before  # Will capture all text from after 'Send print files out of INNOPAC' to before 'Choose one'
		numberToEnterString = fnDeterminerInstance.determineFileNumber(textToExamine)
		fileToSendName = fnDeterminerInstance.foundFileName

		if(numberToEnterString != "-1"):  # means a legit file was found
			try:
				child.send("F")  # F > FTP a print file to another system
				child.send(numberToEnterString)  # i.e."2 > jta_20060329_134110.p"
				child.expect("INNOPAC FILE TRANSFER PROGRAM")
				child.expect("Remote machine ID")  # "Choose one (F,R,Y,Q)"
			except:
				newLogEntry = screenNameText + "FAILURE"
				self.endProgram(newLogEntry, "exceptionFailure", child)
		else:
			newLogEntry = screenNameText + "NO PAGE-SLIP FILES TO SEND" + "\n" + "closing session"
			if(self.debug == "on"):
				print newLogEntry
			self.endProgram(newLogEntry, "success", child)

		# if I get here all was well
		newLogEntry = screenNameText + "success"
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# access 'Send print files out of innopac' screen
		#######

		screenNameText = "access 'Send print files out of innopac' screen (2nd time) step - "

		try:
			child.sendline(prefsInstance.ftpTargetHost)
			child.sendline(prefsInstance.ftpLogin)
			child.sendline(prefsInstance.ftpPassword)
			child.sendline(prefsInstance.ftpDestinationPath)
			option = child.expect(["Transfer completed", "File not transferred"])
		except:
			newLogEntry = screenNameText + "FAILURE - (substep A)"
			self.endProgram(newLogEntry, "exceptionFailure", child)

		if( option == 0 ):
			try:
				child.send(" ")  # Press <SPACE> to continue
				child.send(" ")  # Press <SPACE> to continue
				child.expect( "Send print files out of INNOPAC using FTP" )
				child.expect( "Choose one" )  # Choose one (F,R,Y,Q)
			except:
				newLogEntry = screenNameText + "FAILURE - (substep B) - but file '" + fileToSendName + "' WAS sent"
				self.endProgram(newLogEntry, "exceptionFailure", child)

			newLogEntry = screenNameText + "success - file sent: " + fileToSendName

		if( option == 1 ):
			newLogEntry = screenNameText + "FAILURE: PROBLEM: 'File not transferred"  # I saw this message once when destination server hadn't been configured to accept connections from Josiah's IP address
			newLogEntry = newLogEntry + "\n" + "closing session"
			self.endProgram(newLogEntry, "problem", child)

		# if I get here all was well
		self.log = self.log + "\n" + newLogEntry
		if(self.debug == "on"):
			print newLogEntry



		#######
		# delete existing file -- after confirming that number is still the same
		#######

		screenNameText = "deleting sent file step - "

		fnDeterminerInstance = NumberDeterminer.NumberDeterminer()
		textToExamine = child.before  # Will capture all text from after 'Send print files out of INNOPAC' to before 'Choose one'
		numberToEnterStringChecked = fnDeterminerInstance.determineFileNumber(textToExamine)
		fileToDeleteName = fnDeterminerInstance.foundFileName

		# also get number of files for possible extra alert message
		filesToFtpCount = fnDeterminerInstance.determineFileCount(textToExamine)

		if( fileToDeleteName == fileToSendName ):
			try:
				child.send("R")  # R > REMOVE files
				child.expect( "Input numbers" )  # "Input numbers of files to be removed:"
				child.sendline( numberToEnterStringChecked )
				child.expect( "Remove file" )  # Remove file barttest.p? (y/n)
				child.send("y")  # Remove file barttest.p? (y/n)
				child.expect( "FTP a print file" )  # F > FTP a print file to another system
			except:
				newLogEntry = screenNameText + "FAILURE"
				self.endProgram(newLogEntry, "exceptionFailure", child)
		else:
			newLogEntry = screenNameText + "FAILURE - fileToDelete '" + fileToDeleteName + "' doesn't match fileSent '" + fileToSendName + "'" + "\n" + "closing session"
			if(self.debug == "on"):
				print newLogEntry
			self.endProgram(newLogEntry, "problem", child)

		newLogEntry = screenNameText + "success"
		self.log = self.log + "\n" + newLogEntry
		if( filesToFtpCount > 8 ):
			newLogEntry = "WARNING: the 'files to FTP' list is getting big; ask folk to delete their unused files."
			self.log = self.log + "\n\n" + newLogEntry + "\n"
		if(self.debug == "on"):
			print newLogEntry



		#######
		# close
		#######

		newLogEntry = "closing session"
		if(self.debug == "on"):
			print newLogEntry
			print ""
			print "My pid:"
			print str(child.pid)
			print ""

		if(self.debug == "on"):
			sys.stdout.flush()

		self.endProgram(newLogEntry, "success", child)



	def endProgram(self, newLogEntry, message, child):

		import os
		import sys
		import DatePrepper
		import Emailer
		import Prefs

		datePrepperInstance = DatePrepper.DatePrepper()
		emailerInstance = Emailer.Emailer()
		prefsInstance = Prefs.Prefs()

		os.popen( "kill -9 " + str(child.pid) )

		self.log = self.log + "\n" + newLogEntry
		if( message == "exceptionFailure"):
			errorMessage = "---"  + "\n"
			errorMessage = errorMessage + "Error - info start:" + "\n"
			errorMessage = errorMessage + str(child) + "\n"
			errorMessage = errorMessage + "" + "\n"
			errorMessage = errorMessage + str(child.before) + "\n"
			errorMessage = errorMessage + "Error - info end." + "\n"
			errorMessage = errorMessage + "---"
			self.log = self.log + "\n" + errorMessage

		dateAndTimeText = datePrepperInstance.obtainDate()
		self.log = self.log + "\n\n" + "Automated ssh session ending at " + dateAndTimeText
		self.log = self.log + "\n\n" + "-------"

		print self.log

		message = self.log
		emailerInstance.headerSubject = prefsInstance.headerSubject_fileTransfer
		emailerInstance.sendEmail(message)

		sys.exit()



if __name__ == "__main__":
	controllerInstance = FileTransferController()
	controllerInstance.runCode()



# bottom
