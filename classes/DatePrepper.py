# -*- coding: utf-8 -*-

"""
Obtains date in needed formats.
"""

from __future__ import unicode_literals

import string, time


class DatePrepper( object ):

    def __init__( self ):
       self.timeToFormat = ''

    def obtainDate(self):
        """ Preps date for initial log entry.
            Called by FileSaveController.run_code() and FileTransferController.run_code() """
        if len(self.timeToFormat) == 0:
            theTime = time.localtime()
        else:
            theTime = self.timeToFormat
        formattedTime = time.strftime( '%a %b %d %H:%M:%S %Z %Y', theTime )
        return formattedTime

    def obtainMiniNameTwo(self):
        """ Prepares date-based filename in format `jta_20050802_090539`.
            Called by FileSaveController.run_code()
            Resource: <http://docs.python.org/lib/module-time.html> """
        if len(self.timeToFormat) == 0:
            rawDateInfo = time.localtime()
        else:
            rawDateInfo = self.timeToFormat
        fourDigitYear = time.strftime( '%Y', rawDateInfo )
        twoDigitMonth = time.strftime( '%m', rawDateInfo )
        twoDigitDay = time.strftime( '%d', rawDateInfo )
        twoDigitHour = time.strftime( '%H', rawDateInfo )
        twoDigitMinute = time.strftime( '%M', rawDateInfo )
        twoDigitSecond = time.strftime( '%S', rawDateInfo )
        formattedTime = 'jta_' + fourDigitYear + twoDigitMonth + twoDigitDay + '_' + twoDigitHour + twoDigitMinute + twoDigitSecond
        return formattedTime

    # end class DatePrepper
