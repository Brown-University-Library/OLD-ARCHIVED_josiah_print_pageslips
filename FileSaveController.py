# top


'''
Part of Josiah-to-Annex Telnet code.
Manage export of Annex requests to Annex server.
'''

import json, logging, os, pprint, sys
from josiah_print_pageslips.classes.Emailer import Mailer



## settings from env/activate
LOG_PATH = os.environ['PGSLP__LOG_PATH']
LOG_LEVEL = os.environ['PGSLP__LOG_LEVEL']  # 'DEBUG' or 'INFO'

## log config
log_level = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
logging.basicConfig(
    # filename=LOG_PATH, level=log_level[LOG_LEVEL],
    filename=LOG_PATH, level=log_level[LOG_LEVEL],
    format=u'[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt=u'%d/%b/%Y %H:%M:%S'
    )
logger = logging.getLogger(__name__)



class FileSaveController( object ):


    def __init__( self ):
        self.PATH_ADDITIONS = json.loads( os.environ['PGSLP__PATH_ADDITIONS_JSON'] )
        self.ssh_target_host = os.environ['PGSLP__SSH_TARGET_HOST']
        self.login_name = os.environ['PGSLP__LOGIN_NAME']
        self.login_password = os.environ['PGSLP__LOGIN_PASSWORD']
        self.initialsName = os.environ['PGSLP__INITIALS_NAME']
        self.initialsPassword = os.environ['PGSLP__INITIALS_PASSWORD']
        self.datePrepperInstance = None
        self.numberDeterminerInstance = None


    def runCode(self):

        logger.info( u'starting runCode()' )

        #######
        # setup environment
        #######

        for path in self.PATH_ADDITIONS:
            sys.path.append( path )

        import pexpect
        from public_code.classes import DatePrepper, NumberDeterminer

        self.datePrepperInstance = DatePrepper.DatePrepper()
        self.numberDeterminerInstance = NumberDeterminer.NumberDeterminer()

        dateAndTimeText = self.datePrepperInstance.obtainDate()
        logger.info( u'Automated ssh session starting at `%s`' % dateAndTimeText )


        #######
        # connect
        #######

        child = None
        try:
            child = pexpect.spawn('ssh ' + self.login_name + "@" + self.ssh_target_host)
            if( LOG_LEVEL == 'DEBUG' ):
                child.logfile = sys.stdout
            child.delaybeforesend = .5
            logger.info( u'connect via ssh step - success' )
        except Exception as e:
            message = u'connect via ssh FAILED, exception, `%s`' % unicode(repr(e))
            logger.error( message )
            self.endProgram( message=message, type='problem', child=child )


        #######
        # authenticate
        #######

        try:
            child.expect('password: ')
            child.sendline( login_password )
            logger.info( u'login step - success' )
        except:
            message = u'Login step FAILED'
            self.endProgram( message=message, type='problem', child=child )


        #######
        # access *** MAIN MENU ***
        #######

        screenNameText = "access 'Main menu' screen step - "
        try:
            child.expect('Choose one')  # "Choose one (S,D,C,M,A,Q)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)



        #######
        # access *** CIRCULATION SUBSYSTEM ***
        #######

        screenNameText = "access 'Circulation' screen step - "
        try:
            child.send('C')  # "C > CIRCULATION subsystem"
            child.expect("key your initials")
            child.sendline(initialsName)
            child.expect("key your password")
            child.sendline(initialsPassword)
            child.expect("CIRCULATION SUBSYSTEM")
            child.expect("Choose one")  # "Choose one (O,I,R,H,D,V,P,A,Q)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)



        #######
        # access *** ADDITIONAL CIRCULATION FUNCTIONS ***
        #######

        screenNameText = "access 'Additional circulation' screen step - "
        try:
            child.send('A')  # "A > ADDITIONAL circulation functions"
            child.expect("ADDITIONAL CIRCULATION FUNCTIONS")
            child.expect("Choose one")  # "Choose one (F,H,R,L,I,C,N,E,T,U,D,B,P,S,O,Q)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)


        #######
        # access *** PRINT CIRCULATION NOTICES ***
        #######

        screenNameText = "access 'Print circulation notices' screen step - "
        try:
            child.send('N')  # "N > Print circulation NOTICES"
            child.expect("key your initials")
            child.sendline(initialsName)
            child.expect("key your password")
            child.sendline(initialsPassword)
            child.expect("PRINT CIRCULATION NOTICES")
            child.expect("Choose one")  # "Choose one (O,X,R,H,P,L,B,S,C,Q)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)


        #######
        # access 'Print page slips - start'
        #######

        screenNameText = "access 'Print page slips - start' screen step - "
        option = ""
        try:
            child.send('P')  # "P > Print PAGING slips"
            option = child.expect(["Choose one", "Someone is printing page slips"])  # "Choose one (1,2,3,Q)"
            if(option == 0):
                newLogEntry = screenNameText + "success"
            if(option == 1):
                newLogEntry = screenNameText + "FAILURE: PROBLEM: 'Someone is printing page slips'"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)

        if(option == 1):
            newLogEntry = "closing session"
            self.endProgram(newLogEntry, "success", child)


        #######
        # access 'Print page slips - preparing notices' screen
        #######

        screenNameText = "access 'Print page slips - preparing notices' screen step - "
        option = ""
        try:
            child.send('3')  # "3 > Prepare notices for Annex"
            child.expect("notices for Annex")
            option = child.expect( ["page slip file creation complete", "no page slip notices", "SPACE"] )
            if(option == 0):
                newLogEntry = screenNameText + "success"
            if(option == 1):
                newLogEntry = screenNameText + "NO PAGE-SLIP NOTICES TO PRINT"
            if(option == 2):
                newLogEntry = screenNameText + "lots of cancellations, proceeding"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)

        if(option == 1):
            newLogEntry = "closing session"
            self.endProgram(newLogEntry, "success", child)


        #######
        # access 'Print page slips - notices to process' screen
        #######

        screenNameText = "access 'Print page slips - notices to process' screen step - "
        try:
            child.send(' ')  # "Press <SPACE> to continue"
            child.expect("BEGIN printing paging slips")
            child.expect("Choose one")  # "Choose one (B,S,P,A,N,C,T,Q)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)


        #######
        # access 'Print page slips - begin printing' screen
        #######

        screenNameText = "access 'Print page slips - begin printing' screen step - "
        try:
            child.send('B')  # "B > BEGIN printing paging slips starting with item 1"
            child.expect("File save")
            child.expect("Choose one")  # "Choose one (1-4)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)


        #######
        # access 'Print page slips - confirm file-save' screen
        #######
        screenNameText = "access 'Print page slips - confirm file-save' screen step - "
        try:
            child.send('2')  # "2 > File save"
            child.expect("Is File save ready")  # "Is File save ready?  (y/n)"
            newLogEntry = screenNameText + "success"
            self.log = self.log + "\n" + newLogEntry
            if(self.debug == "on"):
                print newLogEntry
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)


        #######
        # access 'Print page slips - name file' screen
        #######
        screenNameText = "access 'Print page slips - name file' screen step - "
        try:
            child.send('y')  # "Is File save ready?  (y/n)"
            child.expect("File_name")  # "Is File save ready?  (y/n) yFile_name : "
        except:
            newLogEntry = screenNameText + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)

        newLogEntry = screenNameText + "success"
        self.log = self.log + "\n" + newLogEntry
        if(self.debug == "on"):
            print newLogEntry


        #######
        # access 'Print page slips - certify printout' screen (filename, 'y', & space)
        #######
        screenNameText = "access 'Print page slips - certify printout' screen step"

        fileName = self.datePrepperInstance.obtainMiniNameTwo()  # returns in format "jta_20050802_090539"

        try:  # substep A
            child.sendline(fileName)  # Is File save ready?  (y/n) yFile_name :
            child.expect("the printout OK")
            textToExamineForNoticesNumber = child.before  # Will capture all text from after 'Is File save ready?  (y/n) yFile_name : ' to before 'the printout OK'
        except:
            newLogEntry = screenNameText + "A - " + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)
        try:  # substep B
            child.send("y")  # Was the printout OK? (y/n)
            child.expect("removed from print file")
        except:
            newLogEntry = screenNameText + "B - " + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)
        try:  # substep C
            child.send(" ")  # Press <SPACE> to continue
            child.expect("PRINT CIRCULATION NOTICES")
        except:
            newLogEntry = screenNameText + "C - " + "FAILURE"
            self.endProgram(newLogEntry, "exceptionFailure", child)

        # numberDeterminerInstance = NumberDeterminer.NumberDeterminer()
        self.numberDeterminerInstance.figureNoticesNumber(textToExamineForNoticesNumber)
        newLogEntry = screenNameText + " - success, " + numberDeterminerInstance.noticesPrintedText

        self.log = self.log + "\n" + newLogEntry
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


    def endProgram( self, message, type, child ):
        """ Ends script in consistent manner.
            Called by various run_code() steps. """

        logger.debug( u'starting endProgram()' )
        logger.debug( u'message, `%s`' % message )
        logger.debug( u'type, `%s`' % type )
        logger.debug( u'child, `%s`' % child )

        if child == None:  # happens on failed connection
            logger.info( u'no pexpect child' )
        else:
            try:
                os.popen( 'kill -9 ' + str(child.pid) )
                logger.debug( u'script process successfully ended' )
            except Exception as e:
                logger.error( u'Problem killing process, exception, `%s`' % unicode(repr(e)) )

        if type == 'problem':
            subject = u'josiah-pageslip processing problem'
            m = Mailer( subject, message )
            m.send_email()
            logger.debug( u'email sent' )

        logger.info( u'Automated ssh session ending' )

        sys.exit()



if __name__ == "__main__":
    controllerInstance = FileSaveController()
    controllerInstance.runCode()
