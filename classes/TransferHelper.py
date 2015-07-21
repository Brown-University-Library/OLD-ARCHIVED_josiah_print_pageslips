# -*- coding: utf-8 -*-

""" Contains helpers for FileTransferController.py """

from __future__ import unicode_literals

import logging, re


log = logging.getLogger(__name__)


class FileNumberGrabber( object ):

    def __init__( self ):
        self.found_file_name = ''

    def grab_file_number( self, screen_text ):
        """ Grabs the integer representing the file to FTP to the LAS server.
            Called by FileTransferController.run_code()
            Flow...
            - find fileName
            - find position of fileName
            - backup 5 positions
            - capture next 3 characters
            - remove possible trailing space
            - remove possible preceeding 'H'
            - what's left is our number """
        self.found_file_name = self._find_file_name( screen_text )
        if not self.found_file_name:
            return '-1'
        file_number = self._determine_file_number( screen_text )
        log.debug( 'file_number, `%s`' % file_number )
        return file_number

    def _find_file_name( self, screen_text ):
        """ Searches for filename by regex & sets it.
            Called by grab_file_number() """
        regex_pattern = """
            (jta_20)        # initial prefix
            [0-9][0-9]      # rest of year
            [0-9][0-9]      # month
            [0-9][0-9]      # day
            (_)             # separator
            [0-9][0-9]      # hour
            [0-9][0-9]      # minute
            [0-9][0-9]      # second
            (\.)(p)         # suffix
            """
        search_result = re.search( regex_pattern, screen_text, re.VERBOSE )
        if search_result:
            self.found_file_name = search_result.group()
        return self.found_file_name

    def _determine_file_number( self, screen_text ):
        """ Finds and returns file-number given file-name.
            Called by grab_file_number() """
        foundFileNamePosition = screen_text.find( self.found_file_name )
        numberStartPosition = foundFileNamePosition - 5
        textSectionA = screen_text[numberStartPosition:numberStartPosition+3]
        textSectionB = textSectionA.strip()  # removes leading and trailing whitespace
        if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
            textSectionC = textSectionB[1:]
        else:
            textSectionC = textSectionB
        return textSectionC



    # def grab_file_number( self, screen_text ):
    #     """ Grabs the integer representing the file to FTP to the LAS server.
    #         Called by FileTransferController.run_code() """
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

    #     searchResult = re.search(regexPattern, screen_text, re.VERBOSE)

    #     fileName = "init"
    #     returnVal = "init"

    #     if( searchResult == None):
    #         returnVal = "-1"
    #     else:
    #         fileName = searchResult.group()
    #         self.found_file_name = fileName

    #     # find position of fileName and deduce fileName number

    #     if( returnVal != "-1" ):
    #         foundFileNamePosition = string.find( screen_text, fileName )
    #         numberStartPosition = foundFileNamePosition - 5
    #         textSectionA = screen_text[numberStartPosition:numberStartPosition+3]
    #         textSectionB = string.strip(textSectionA)  # removes leading and trailing whitespace
    #         if(textSectionB[0:1] == 'H'):  # removes possible 'H' character
    #             textSectionC = textSectionB[1:]
    #         else:
    #             textSectionC = textSectionB
    #         returnVal = textSectionC

    #     return returnVal

    # end class FileNumberGrabber
