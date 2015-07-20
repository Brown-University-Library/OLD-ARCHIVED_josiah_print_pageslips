# -*- coding: utf-8 -*-

"""
Tests josiah_print_pageslips.classes.DatePrepper
"""

from __future__ import unicode_literals

import datetime, unittest
from josiah_print_pageslips.classes import DatePrepper


class DatePrepperTest( unittest.TestCase ):

    def testPrepDate_sentTime(self):
        """ Tests datetime formatting for given date. """
        date_prepper = DatePrepper.DatePrepper()
        date_prepper.dt_tm_obj = datetime.datetime( 2005, 7, 13, 13, 41, 39 )
        result = date_prepper.obtain_date()
        self.assertEqual( unicode, type(result) )
        self.assertEqual( 'Wed Jul 13 13:41:39 EDT 2005', result )

    def testPrepDate_noSentTime(self):
        """ Tests datetime formatting returns a valid datetime string when no date given. """
        date_prepper = DatePrepper.DatePrepper()
        dt_tm_string = date_prepper.obtain_date()
        self.assertEqual( unicode, type(dt_tm_string) )
        date_obj_from_dt_tm_string = datetime.datetime.strptime( dt_tm_string, '%a %b %d %H:%M:%S EDT %Y' ).date()
        today_date = datetime.date.today()
        self.assertEqual( today_date, date_obj_from_dt_tm_string )

    def testobtain_mini_name_withSentDate(self):
        """ Tests datetime formatting for filename. """
        date_prepper = DatePrepper.DatePrepper()
        date_prepper.dt_tm_obj = datetime.datetime( 2005, 8, 2, 9, 5, 39 )  # '2005 Aug 2 09:05:39 EDT 2005'
        result = date_prepper.obtain_mini_name()
        self.assertEqual( unicode, type(result) )
        self.assertEqual( 'jta_20050802_090539', result )


if __name__ == '__main__':
    unittest.main()
