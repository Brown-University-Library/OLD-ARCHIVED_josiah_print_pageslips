# -*- coding: utf-8 -*-

"""
Manages creation of iii-millennium pageslips for Annex-requests.
- Part 1 of 2 of Josiah-to-Annex Telnet code.
- Assumes:
  - virtual environment set up
  - site-packages `requirements.pth` file adds josiah_print_pageslips enclosing-directory to sys path.
"""

from __future__ import unicode_literals

import json, logging, os, pprint, sys
import pexpect
from josiah_print_pageslips.classes.Emailer import Mailer
from josiah_print_pageslips.classes.DatePrepper import DatePrepper
from josiah_print_pageslips.classes.SaveHelper import PageslipCounter


## instances
date_prepper = DatePrepper()
counter = PageslipCounter()


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



class FileSaveController( object ):


    def __init__( self ):
        self.ssh_target_host = os.environ['PGSLP__SSH_TARGET_HOST']
        self.login_name = os.environ['PGSLP__LOGIN_NAME']
        self.login_password = os.environ['PGSLP__LOGIN_PASSWORD']
        self.initials_name = os.environ['PGSLP__INITIALS_NAME']
        self.initials_password = os.environ['PGSLP__INITIALS_PASSWORD']


    def run_code(self):

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
        # access *** CIRCULATION SUBSYSTEM ***
        #######

        screen_name_text = "access 'Circulation' screen step"
        try:
            child.send('C')  # "C > CIRCULATION subsystem"
            child.expect("key your initials")
            child.sendline( self.initials_name )
            child.expect("key your password")
            child.sendline( self.initials_password )
            child.expect("CIRCULATION SUBSYSTEM")
            child.expect("Choose one")  # "Choose one (O,I,R,H,D,V,P,A,Q)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access *** ADDITIONAL CIRCULATION FUNCTIONS ***
        #######

        screen_name_text = "access 'Additional circulation' screen step"
        try:
            child.send('A')  # "A > ADDITIONAL circulation functions"
            child.expect("ADDITIONAL CIRCULATION FUNCTIONS")
            child.expect("Choose one")  # "Choose one (F,H,R,L,I,C,N,E,T,U,D,B,P,S,O,Q)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access *** PRINT CIRCULATION NOTICES ***
        #######

        screen_name_text = "access 'Print circulation notices' screen step"
        try:
            child.send('N')  # "N > Print circulation NOTICES"
            child.expect("key your initials")
            child.sendline( self.initials_name )
            child.expect("key your password")
            child.sendline( self.initials_password )
            child.expect("PRINT CIRCULATION NOTICES")
            child.expect("Choose one")  # "Choose one (O,X,R,H,P,L,B,S,C,Q)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - start'
        #######

        screen_name_text = "access 'Print page slips - start' screen step"
        option = ''
        try:
            child.send('P')  # "P > Print PAGING slips"
            option = child.expect( ["Choose one", "Someone is printing page slips"] )  # "Choose one (1,2,3,Q)"
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        if(option == 0):
            logger.info( '%s - success' % screen_name_text )
        if(option == 1):
            message = '%s - FAILURE; Problem: Someone is printing page-slips; this run of the script will stop now.'
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - preparing notices' screen
        #######

        screen_name_text = "access 'Print page slips - preparing notices' screen step"
        option = ''
        try:
            child.send('3')  # "3 > Prepare notices for Annex"
            child.expect("notices for Annex")
            option = child.expect( ["page slip file creation complete", "no page slip notices", "SPACE"] )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        if(option == 0):
            logger.info( '%s - success' % screen_name_text )
        if(option == 1):
            message = '%s - NO PAGE-SLIP NOTICES TO PRINT' % screen_name_text
            self.endProgram( message=message, message_type='success', child=child )
        if(option == 2):
            logger.info( '%s - success (lots of cancellations, proceeding)' % screen_name_text )


        #######
        # access 'Print page slips - notices to process' screen
        #######

        screen_name_text = "access 'Print page slips - notices to process' screen step"
        try:
            child.send(' ')  # "Press <SPACE> to continue"
            child.expect("BEGIN printing paging slips")
            child.expect("Choose one")  # "Choose one (B,S,P,A,N,C,T,Q)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - begin printing' screen
        #######

        screen_name_text = "access 'Print page slips - begin printing' screen step"
        try:
            child.send('B')  # "B > BEGIN printing paging slips starting with item 1"
            child.expect("File save")
            child.expect("Choose one")  # "Choose one (1-4)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - confirm file-save' screen
        #######
        screen_name_text = "access 'Print page slips - confirm file-save' screen step"
        try:
            child.send('2')  # "2 > File save"
            child.expect("Is File save ready")  # "Is File save ready?  (y/n)"
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - name file' screen
        #######
        screen_name_text = "access 'Print page slips - name file' screen step"
        try:
            child.send('y')  # "Is File save ready?  (y/n)"
            child.expect("File_name")  # "Is File save ready?  (y/n) yFile_name : "
            logger.info( '%s - success' % screen_name_text )
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( screen_name_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )


        #######
        # access 'Print page slips - certify printout' screen (filename, 'y', & space)
        #######
        screen_name_text = "access 'Print page slips - certify printout' screen step"

        fileName = date_prepper.obtain_mini_name()  # returns in format "jta_20050802_090539"

        substep_text = '%s - A' % screen_name_text
        try:  # substep A
            child.sendline(fileName)  # Is File save ready?  (y/n) yFile_name :
            child.expect("the printout OK")
            textToExamineForNoticesNumber = child.before  # Will capture all text from after 'Is File save ready?  (y/n) yFile_name : ' to before 'the printout OK'
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( substep_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        substep_text = '%s - B' % screen_name_text
        try:  # substep B
            child.send("y")  # Was the printout OK? (y/n)
            child.expect("removed from print file")
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( substep_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        substep_text = '%s - C' % screen_name_text
        try:  # substep C
            child.send(" ")  # Press <SPACE> to continue
            child.expect("PRINT CIRCULATION NOTICES")
        except Exception as e:
            message = '%s - FAILED, exception, `%s`' % ( substep_text, unicode(repr(e)) )
            self.endProgram( message=message, message_type='problem', child=child )

        pageslips_count = counter.count_pageslips( textToExamineForNoticesNumber )
        logger.info( '%s - success - pageslips printed: %s' % (screen_name_text, pageslips_count) )


        #######
        # close
        #######

        logger.info( 'closing session; pid, `%s`' % unicode(child.pid) )
        sys.stdout.flush()
        self.endProgram( message='closing session', message_type='success', child=child )

        # end def run_code()


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
                command = 'kill -9 %s' % child.pid
                os.popen( command.encode('utf-8') )
                logger.debug( 'script process successfully ended' )
            except Exception as e:
                logger.error( 'Problem killing process, exception, `%s`' % unicode(repr(e)) )

        if message_type == 'problem':
            subject = 'josiah-pageslip processing problem'
            m = Mailer( subject, message )
            m.send_email()

        logger.info( 'Automated ssh session ending' )

        sys.exit()



if __name__ == "__main__":
    controllerInstance = FileSaveController()
    controllerInstance.run_code()
