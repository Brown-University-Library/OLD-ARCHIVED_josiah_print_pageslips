# -*- coding: utf-8 -*-

""" Obtains date in needed formats.
    Called by both FileSaveController.py and FileTransferController.py """

from __future__ import unicode_literals

import datetime


class DatePrepper( object ):

    def __init__( self, dt_tm_obj=None ):
       self.dt_tm_obj = None  # allows date obj to be passed in for testing

    def obtain_date(self):
        """ Preps date for initial log entry in format `Wed Jul 13 13:41:39 EDT 2005`.
            Called by FileSaveController.run_code() and FileTransferController.run_code() """
        if not self.dt_tm_obj:
            self.dt_tm_obj = datetime.datetime.now()
        formatted_utf8_time = datetime.datetime.strftime( self.dt_tm_obj, '%a %b %d %H:%M:%S EDT %Y' )
        formatted_time = formatted_utf8_time.decode( 'utf-8' )
        return formatted_time

    def obtain_mini_name(self):
        """ Prepares date-based filename in format `jta_20050802_090539`.
            Called by FileSaveController.run_code() """
        if not self.dt_tm_obj:
            self.dt_tm_obj = datetime.datetime.now()
        formatted_utf8_time = datetime.datetime.strftime( self.dt_tm_obj, 'jta_%Y%m%d_%H%M%S' )
        formatted_time = formatted_utf8_time.decode( 'utf-8' )
        return formatted_time

    # end class DatePrepper
