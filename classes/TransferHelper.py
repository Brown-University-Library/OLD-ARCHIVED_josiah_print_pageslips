# -*- coding: utf-8 -*-

""" Contains helpers for FileTransferController.py """

from __future__ import unicode_literals

import logging, re


log = logging.getLogger(__name__)


class FileCounter( object ):

    def __init__( self ):
        self.regex_pattern = """
            (;1H)       # prefix
            [0-9]       # targetNumber
            [ ][>][ ]   # suffix
            """
        self.highestNumber = 0

    def count_ftp_list_files( self, screen_text ):
        """ Determines count of files in ftp list.
            Called by FileTransferController.run_code() to determine whether to alert admins that ftp-list is getting too large.
            Flow...
            - find pattern in screen_text
            - store that number
            - delete all text up to and including this find.
            - look again.
            - if found, store number and repeat until no more finds occur.
            - at this point, the stored number is the count. """
        text_to_process = screen_text
        loop_flag = 'continue'
        while( loop_flag == 'continue' ):
            search_result = re.search( self.regex_pattern, text_to_process, re.VERBOSE )
            if search_result == None:
                break
            else:
                text_to_process = self._process_search_result( search_result, text_to_process )
        return int(self.highestNumber)

    def _process_search_result( self, search_result, text_to_process ):
        """ Grabs current-count in found_text, and deletes all text up to and including found_text for further examination.
            Returns remaining text_to_process.
            Called by count_ftp_list_files() """
        found_text = search_result.group()
        self.highestNumber = found_text[3:4]
        foundtext_start_position = text_to_process.find( found_text )
        foundtext_length = len( found_text )
        text_to_process = text_to_process[ foundtext_start_position + foundtext_length: ]  # grabs rest of text after found_text
        return text_to_process

    # end class FileCounter


class FileNumberGrabber( object ):

    def __init__( self ):
        self.found_file_name = ''

    def grab_file_number( self, screen_text ):
        """ Grabs the integer representing the file to FTP to the LAS server.
            Example string: `2 > jta_20060329_134110.p`
            Called by FileTransferController.run_code()
            Flow...
            - find fileName
            - find position of fileName
            - backup 5 positions
            - capture next 3 characters
            - remove possible trailing space
            - remove possible preceeding 'H'
            - what's left is our number """
        log.debug( 'screen_text, ```%s```' % screen )
        self.found_file_name = self._find_file_name( screen_text )
        if not self.found_file_name:
            return '-1'
        file_number = self._determine_file_number( screen_text )
        log.debug( 'file_number, `%s`' % file_number )
        return file_number

    # def _find_file_name( self, screen_text ):
    #     """ Searches for filename by regex & sets it.
    #         Called by grab_file_number() """
    #     regex_pattern = """
    #         (jta_20)        # initial prefix
    #         [0-9][0-9]      # rest of year
    #         [0-9][0-9]      # month
    #         [0-9][0-9]      # day
    #         (_)             # separator
    #         [0-9][0-9]      # hour
    #         [0-9][0-9]      # minute
    #         [0-9][0-9]      # second
    #         (\.)(p)         # suffix
    #         """
    #     search_result = re.search( regex_pattern, screen_text, re.VERBOSE )
    #     if search_result:
    #         self.found_file_name = search_result.group()
    #     return self.found_file_name

    def _find_file_name( self, screen_text ):
        """ Searches for filename by regex & sets it.
            Called by grab_file_number() """
        local_found_file_name = ''
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
            local_found_file_name = search_result.group()
        self.found_file_name = local_found_file_name
        log.debug( 'local_found_file_name, ```%s```' % local_found_file_name )
        return local_found_file_name

    def _determine_file_number( self, screen_text ):
        """ Finds and returns file-number given file-name.
            Called by grab_file_number() """
        file_name_position = screen_text.find( self.found_file_name )
        segment_start_position = file_name_position - 5
        segment_a = screen_text[ segment_start_position: segment_start_position+3 ]
        segment_b = segment_a.strip()  # removes leading and trailing whitespace
        if segment_b[0:1] == 'H':  # removes possible 'H' character
            segment_c = segment_b[1:]
        else:
            segment_c = segment_b
        log.debug( 'returning segement, ```%s```' % segment_c )
        return segment_c

    # end class FileNumberGrabber
