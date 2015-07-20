# -*- coding: utf-8 -*-

"""
Manages export of iii-millennium pageslips to Annex server.
- Part 2 of 2 of Josiah-to-Annex Telnet code.
- Assumes:
  - virtual environment set up
  - site-packages `requirements.pth` file adds josiah_print_pageslips enclosing-directory to sys path.
"""

from __future__ import unicode_literals

import logging, os, sys
import pexpect
from josiah_print_pageslips.classes.Emailer import Mailer
from josiah_print_pageslips.classes.DatePrepper import DatePrepper
from josiah_print_pageslips.classes.NumberDeterminer import NumberDeterminer


## instances
date_prepper = DatePrepper()
number_determiner = NumberDeterminer()


## settings from env/activate
LOG_PATH = os.environ['PGSLP__LOG_PATH']
LOG_LEVEL = os.environ['PGSLP__LOG_LEVEL']  # 'DEBUG' or 'INFO'


## log config
log_level = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
logging.basicConfig(
    filename=LOG_PATH, level=log_level[LOG_LEVEL],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
logger = logging.getLogger(__name__)



class FileTransferController( object ):


    def __init__( self ):
        self.ssh_target_host = os.environ['PGSLP__SSH_TARGET_HOST']
        self.login_name = os.environ['PGSLP__LOGIN_NAME']
        self.login_password = os.environ['PGSLP__LOGIN_PASSWORD']
        self.initials_name = os.environ['PGSLP__INITIALS_NAME']
        self.initials_password = os.environ['PGSLP__INITIALS_PASSWORD']


    def runCode(self):

        logger.info( 'starting run_code()' )

        #######
        # setup environment
        #######

        dateAndTimeText = date_prepper.obtain_date()
        logger.info( 'Automated ssh session starting at `%s`' % dateAndTimeText )


        #######
        # connect
        #######

        child = None
        try:
            child = pexpect.spawn('ssh ' + self.login_name + "@" + self.ssh_target_host)
            if( LOG_LEVEL == 'DEBUG' ):
                child.logfile = sys.stdout
            child.delaybeforesend = .5
            logger.info( 'connect via ssh step - success' )
        except Exception as e:
            message = 'connect via ssh FAILED, exception, `%s`' % unicode(repr(e))
            logger.error( message )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # authenticate
        #######

        try:
            child.expect('password: ')
            child.sendline( self.login_password )
            logger.info( 'login step - success' )
        except Exception as e:
            message = 'Login step FAILED, exception, `%s`' % unicode(repr(e))
            logger.error( message )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access *** MAIN MENU ***
        #######

        screen_name_text = "access 'Main menu' screen step"
        try:
            child.expect('Choose one')  # "Choose one (S,D,C,M,A,Q)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Additional system functions' screen
        #######

        screen_name_text = "access 'Additional system functions' screen step - "
        try:


            1/0


            child.send('A')  # "A > ADDITIONAL system functions"
            child.expect("key your initials")
            child.sendline(initialsName)
            child.expect("key your password")
            child.sendline(initialsPassword)
            child.expect("ADDITIONAL SYSTEM FUNCTIONS")
            child.expect("Choose one")  # "Choose one (C,B,S,M,D,R,E,V,F,N,U,O,A,Q)"
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


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


    def endProgram( self, message, message_type, child ):
        """ Ends script in consistent manner.
            Called by various run_code() steps. """

        logger.debug( 'starting endProgram()' )
        logger.debug( 'message, `%s`' % message )
        logger.debug( 'message_type, `%s`' % message_type )
        logger.debug( 'child, `%s`' % child )

        if child == None:  # happens on failed connection
            logger.info( 'no pexpect child' )
        else:
            try:
                os.popen( 'kill -9 ' + str(child.pid) )
                logger.debug( 'script process successfully ended' )
            except Exception as e:
                logger.error( 'Problem killing process, exception, `%s`' % unicode(repr(e)) )

        if message_type == 'problem':
            subject = 'josiah-pageslip transfer problem'
            m = Mailer( subject, message )
            m.send_email()

        logger.info( 'Automated ssh session ending' )

        sys.exit()


    # def endProgram(self, newLogEntry, message, child):

    #     import os
    #     import sys
    #     import DatePrepper
    #     import Emailer
    #     import Prefs

    #     datePrepperInstance = DatePrepper.DatePrepper()
    #     emailerInstance = Emailer.Emailer()
    #     prefsInstance = Prefs.Prefs()

    #     os.popen( "kill -9 " + str(child.pid) )

    #     self.log = self.log + "\n" + newLogEntry
    #     if( message == "exceptionFailure"):
    #         errorMessage = "---"  + "\n"
    #         errorMessage = errorMessage + "Error - info start:" + "\n"
    #         errorMessage = errorMessage + str(child) + "\n"
    #         errorMessage = errorMessage + "" + "\n"
    #         errorMessage = errorMessage + str(child.before) + "\n"
    #         errorMessage = errorMessage + "Error - info end." + "\n"
    #         errorMessage = errorMessage + "---"
    #         self.log = self.log + "\n" + errorMessage

    #     dateAndTimeText = datePrepperInstance.obtain_date()
    #     self.log = self.log + "\n\n" + "Automated ssh session ending at " + dateAndTimeText
    #     self.log = self.log + "\n\n" + "-------"

    #     print self.log

    #     message = self.log
    #     emailerInstance.headerSubject = prefsInstance.headerSubject_fileTransfer
    #     emailerInstance.sendEmail(message)

    #     sys.exit()



if __name__ == "__main__":
    controllerInstance = FileTransferController()
    controllerInstance.runCode()
