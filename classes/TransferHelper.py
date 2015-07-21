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
        file_name_position = screen_text.find( self.found_file_name )
        segment_start_position = file_name_position - 5
        segment_a = screen_text[ segment_start_position: segment_start_position+3 ]
        segment_b = segment_a.strip()  # removes leading and trailing whitespace
        if segment_b[0:1] == 'H':  # removes possible 'H' character
            segment_c = segment_b[1:]
        else:
            segment_c = segment_b
        return segment_c

    # end class FileNumberGrabber
