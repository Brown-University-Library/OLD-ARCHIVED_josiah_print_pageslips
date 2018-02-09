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
from josiah_print_pageslips.classes.TransferHelper import FileNumberGrabber, FileCounter


## instances
date_prepper = DatePrepper()
file_number_grabber = FileNumberGrabber()
file_counter = FileCounter()


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
        self.ftp_target_host = os.environ['PGSLP__FTP_TARGET_HOST']
        self.ftp_login_name = os.environ['PGSLP__FTP_LOGIN_NAME']
        self.ftp_login_password = os.environ['PGSLP__FTP_LOGIN_PASSWORD']
        self.ftp_destination_path = os.environ['PGSLP__FTP_DESTINATION_PATH']


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

        screen_name_text = "access 'Additional system functions' screen step"
        try:
            child.send('A')  # "A > ADDITIONAL system functions"
            child.expect("key your initials")
            child.sendline( self.initials_name )
            child.expect("key your password")
            child.sendline( self.initials_password )
            child.expect("ADDITIONAL SYSTEM FUNCTIONS")
            child.expect("Choose one")  # "Choose one (C,B,S,M,D,R,E,V,F,N,U,O,A,Q)"
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )
        logger.info( '%s - success' % screen_name_text )


        #######
        # access 'Read/write MARC records' screen
        #######

        screen_name_text = "access 'Read/write marc records' screen step"
        try:
            child.send('M')  # "M > Read/write MARC records"
            child.expect("READ/WRITE MARC RECORDS")
            child.expect("Choose one")  # "Choose one (B,A,S,N,P,X,U,M,L,F,T,Q)"
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )
        logger.info( '%s - success' % screen_name_text )


        #######
        # access 'Send print files out of innopac' screen
        #######

        screen_name_text = "access 'Send print files out of innopac' screen step"
        try:
            child.send('F')  # "F > Send print files out of INNOPAC using FTP"
            child.expect("Send print files out of INNOPAC")
            option = child.expect(["Choose one", "until their combined total size"])  # "Choose one (F,R,Y,Q)"
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        if(option == 0):
            logger.info( '%s - success' % screen_name_text )
        if(option == 1):
            message = '%s - FAILED, problem: total size of files in FTP list is too big' % screen_name_text
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # Build list of files
        # If no JTAs, exit
        # If a JTA exists, remember it -> try to send it -> delete it (basically continue)
        #######


        #######
        # access 'FILE TRANSFER SOFTWARE' screen
        # Look for file to send
        #######

        screen_name_text = "access `FILE TRANSFER SOFTWARE` screen first step of four"
        textToExamine = child.before  # Will capture all text from after 'Send print files out of INNOPAC' to before 'Choose one'
        numberToEnterString = file_number_grabber.grab_file_number( textToExamine )
        fileToSendName = file_number_grabber.found_file_name
        if(numberToEnterString != "-1"):  # means a legit file was found
            try:
                child.send("F")  # F > SFTP a print file to another system
                child.send(numberToEnterString)  # i.e."2 > jta_20060329_134110.p"
                child.expect("FILE TRANSFER SOFTWARE")
                child.expect("ENTER a host")  # `E > ENTER a host`
            except Exception as e:
                message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
                self.endProgram( message=message, message_type='problem', child=child )
            logger.info( '%s - success' % screen_name_text )
        else:
            message = '%s - success, NO PAGE-SLIP FILES TO SEND; closing session' % screen_name_text
            logger.info( '%s - success' % message )
            self.endProgram( message=message, message_type='success', child=child )


        #######
        # still within 'FILE TRANSFER SOFTWARE' screen
        # Initiate the file-transfer
        #######

        screen_name_text = "process `FILE TRANSFER SOFTWARE` screen second step"
        try:
            child.send("E")  # `E > ENTER a host`
            child.expect("Enter host name:")
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )
        logger.info( '%s - success' % screen_name_text )


        #######
        # still within 'FILE TRANSFER SOFTWARE' screen
        # Enter host, username, password
        #######

        screen_name_text = "process `FILE TRANSFER SOFTWARE` screen third step"

        try:
            child.sendline( self.ftp_target_host )
            child.sendline( self.ftp_login_name )
            child.sendline( self.ftp_login_password )
            child.expect("Put File At")  # `Put File At Remote Site`
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # still within 'FILE TRANSFER SOFTWARE' screen
        # Start file-transfer
        #######

        screen_name_text = "process `FILE TRANSFER SOFTWARE` screen fourth step"

        try:
            child.send( 'T' )  # `T > TRANSFER files`
            child.expect( 'Put File At Remote Site' )
            child.expect( 'Enter name of remote file' )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )





        #######
        # still within 'FILE TRANSFER SOFTWARE' screen
        # Start file-transfer
        #######

        screen_name_text = "process `FILE TRANSFER SOFTWARE` screen fifth step"

        try:
            child.sendline( self.ftp_destination_path )
            child.expect( 'Press C to continue' )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )



        #######
        # still within 'FILE TRANSFER SOFTWARE' screen
        # Exit file-transfer area
        #######

        screen_name_text = "access `Send print files out of INNOPAC using FTP` screen (after file-transfer) step"

        try:
            child.send( 'Q' )  # `Q > QUIT`
            child.expect( 'Send print files out of INNOPAC using FTP' )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )






        #######
        # delete existing file -- after confirming that number is still the same
        #######

        screen_name_text = "deleting sent file step"

        textToExamine = child.before  # Will capture all text from after 'Send print files out of INNOPAC' to before 'Choose one'
        numberToEnterStringChecked = file_number_grabber.grab_file_number( textToExamine )
        fileToDeleteName = file_number_grabber.found_file_name
        ## also get number of files for possible extra alert message
        filesToFtpCount = file_counter.count_ftp_list_files( textToExamine )
        if( fileToDeleteName == fileToSendName ):
            try:
                child.send("D")  # `D > REMOVE files`
                child.expect( "Input numbers" )  # "Input numbers of files to be removed:"
                child.sendline( numberToEnterStringChecked )
                child.expect( "Remove file" )  # Remove file barttest.p? (y/n)
                child.send("y")  # Remove file barttest.p? (y/n)
                child.expect( "FTP a print file" )  # F > FTP a print file to another system
            except Exception as e:
                message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
                self.endProgram( message=message, message_type='problem', child=child )
            logger.info( '%s - success' % screen_name_text )
        else:
            message = '%s - FAILURE - fileToDeleteName `%s` doesn\'t match name-of-file-sent `%s`; closing session' % ( screen_name_text, fileToDeleteName, fileToSendName )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # check size of FTP list
        #######

        if( filesToFtpCount > 8 ):
            message = 'WARNING - file transferred fine, but the `files to FTP` list is getting big; ask folk to delete their unused files.'
            subject = 'josiah-pageslip transfer warning'
            m = Mailer( subject, message )
            m.send_email()


        #######
        # close
        #######

        logger.info( 'closing session; pid, `%s`' % unicode(child.pid) )
        sys.stdout.flush()
        self.endProgram( message='closing session', message_type='success', child=child )

        # end def runCode()


    def endProgram( self, message, message_type, child ):
        """ Ends script in consistent manner.
            Called by various run_code() steps. """

        logger.debug( 'starting endProgram()' )
        logger.debug( 'message, `%s`' % message )
        logger.debug( 'message_type, `%s`' % message_type )
        logger.debug( 'child, `%s`' % child )
        logger.debug( 'type(child.pid), `%s`' % type(child.pid) )
        logger.debug( 'child.pid, `%s`' % unicode(repr(child.pid)) )

        if child == None:  # happens on failed connection
            logger.info( 'no pexpect child' )
        else:
            try:
                command = 'kill -9 %s' % child.pid
                os.popen( command.encode('utf-8') )
                logger.debug( 'script process successfully ended' )
            except Exception as e:
                logger.error( 'Problem killing process, exception, `%s`' % unicode(repr(e)) )

        if message_type == 'problem':
            subject = 'josiah-pageslip transfer problem'
            m = Mailer( subject, message )
            m.send_email()

        logger.info( 'Automated ssh session ending' )

        sys.exit()

        # end def endProgram()


if __name__ == "__main__":
    controllerInstance = FileTransferController()
    controllerInstance.runCode()
