# -*- coding: utf-8 -*-

""" Contains helpers for FileTransferController.py """

from __future__ import unicode_literals

import logging


log = logging.getLogger(__name__)


class FileNumberGrabber( object ):

    def __init__( self ):
        self.found_file_name = None

    def grab_file_number( self, screen_text ):
        """ Grabs the integer representing the file to FTP to the LAS server.
            Called by FileTransferController.run_code() """
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
            (jta_20)            # initial prefix
            [0-9][0-9]      # rest of year
            [0-9][0-9]      # month
            [0-9][0-9]      # day
            (_)             # separator
            [0-9][0-9]      # hour
            [0-9][0-9]      # minute
            [0-9][0-9]      # second
            (\.)(p)         # suffix
            """

        searchResult = re.search(regexPattern, screen_text, re.VERBOSE)

        fileName = "init"
        returnVal = "init"

        if( searchResult == None):
            returnVal = "-1"
        else:
            fileName = searchResult.group()
            self.found_file_name = fileName

        # find position of fileName and deduce fileName number

        if( returnVal != "-1" ):
            foundFileNamePosition = string.find( screen_text, fileName )
            numberStartPosition = foundFileNamePosition - 5
            textSectionA = screen_text[numberStartPosition:numberStartPosition+3]
            textSectionB = string.strip(textSectionA)  # removes leading and trailing whitespace
            if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
                textSectionC = textSectionB[1:]
            else:
                textSectionC = textSectionB
            returnVal = textSectionC

        return returnVal

    # end class FileNumberGrabber



    # def determineFileNumber(self, screenText):

    #     # find fileName
    #     # find position of fileName
    #     # backup 5 positions
    #     # capture next 3 characters
    #     # remove possible trailing space
    #     # remove possible preceeding 'H'
    #     # what's left is our number

    #     import re
    #     import string

    #     # find fileName

    #     regexPattern = """
    #         (jta_20)            # initial prefix
    #         [0-9][0-9]      # rest of year
    #         [0-9][0-9]      # month
    #         [0-9][0-9]      # day
    #         (_)             # separator
    #         [0-9][0-9]      # hour
    #         [0-9][0-9]      # minute
    #         [0-9][0-9]      # second
    #         (\.)(p)         # suffix
    #         """

    #     searchResult = re.search(regexPattern, screenText, re.VERBOSE)

    #     fileName = "init"
    #     returnVal = "init"

    #     if( searchResult == None):
    #         returnVal = "-1"
    #     else:
    #         fileName = searchResult.group()
    #         self.foundFileName = fileName

    #     # find position of fileName and deduce fileName number

    #     if( returnVal != "-1" ):
    #         foundFileNamePosition = string.find( screenText, fileName )
    #         numberStartPosition = foundFileNamePosition - 5
    #         textSectionA = screenText[numberStartPosition:numberStartPosition+3]
    #         textSectionB = string.strip(textSectionA)  # removes leading and trailing whitespace
    #         if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
    #             textSectionC = textSectionB[1:]
    #         else:
    #             textSectionC = textSectionB
    #         returnVal = textSectionC

    #     return returnVal
