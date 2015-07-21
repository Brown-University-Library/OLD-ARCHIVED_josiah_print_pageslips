# -*- coding: utf-8 -*-

"""
Tests josiah_print_pageslips.classes.SaveHelper
"""

from __future__ import unicode_literals

import unittest
from josiah_print_pageslips.classes import SaveHelper


class SaveHelperTest( unittest.TestCase ):

    def testFigureNoticesNumber_goodInput(self): # contains 'notices' (plural)
        """determines the number of notices printed by looking at the telnet screen info"""

        notNumDetInstance = NumberDeterminer.NumberDeterminer()
        textOfScreen = 'jta_aug24_0840[16;6H[JPress <ESCAPE> to STOP printing[19;6H[KNow printing 1"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 2"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 3"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 4"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 5"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 6"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[14;6H[JPrinting Complete[15;6H6 notices printed.[16;6HWas the printout OK? (y/n) '

        expected = "6"
        returned = notNumDetInstance.figureNoticesNumber(textOfScreen)
        self.assertEqual( expected, returned, "returned is: " + str(returned) )

        expected = "6 notices printed"
        returned = notNumDetInstance.noticesPrintedText
        self.assertEqual( expected, returned, "returned is: " + str(returned) )



    def testFigureNoticesNumber_goodDifferentInput(self): # contains 'notice' (singular)
        """determines the number of notices printed by looking at the telnet screen info"""

        notNumDetInstance = NumberDeterminer.NumberDeterminer()
        textOfScreen = 'jta_aug25_0844[16;6H[JPress <ESCAPE> to STOP printing[19;6H[KNow printing 1"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[14;6H[JPrinting Complete[15;6H1 notice printed.[16;6HWas the printout OK? (y/n)'

        expected = "1"
        returned = notNumDetInstance.figureNoticesNumber(textOfScreen)
        self.assertEqual( expected, returned, "returned is: " + str(returned) )

        expected = "1 notice printed"
        returned = notNumDetInstance.noticesPrintedText
        self.assertEqual( expected, returned, "returned is: " + str(returned) )



    def testFigureNoticesNumber_badInput(self):
        """determines the number of notices printed by looking at the telnet screen info"""

        notNumDetInstance = NumberDeterminer.NumberDeterminer()
        textOfScreen = 'blah'

        expected = "noNumFound"
        returned = notNumDetInstance.figureNoticesNumber(textOfScreen)
        self.assertEqual( expected, returned, "returned is: " + str(returned) )

        expected = ""
        returned = notNumDetInstance.noticesPrintedText
        self.assertEqual( expected, returned, "returned is: " + str(returned) )
