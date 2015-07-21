# -*- coding: utf-8 -*-

"""
Tests josiah_print_pageslips.classes.SaveHelper
"""

from __future__ import unicode_literals

import logging, os, unittest
from josiah_print_pageslips.classes.SaveHelper import PageslipCounter


## settings from env/activate
LOG_PATH = os.environ['PGSLP__LOG_PATH']
LOG_LEVEL = os.environ['PGSLP__LOG_LEVEL']  # 'DEBUG' or 'INFO'


## logging
log_level = { 'DEBUG': logging.DEBUG, 'INFO': logging.INFO }
logging.basicConfig(
    filename=LOG_PATH, level=log_level[LOG_LEVEL],
    format='[%(asctime)s] %(levelname)s [%(module)s-%(funcName)s()::%(lineno)d] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S'
    )
logger = logging.getLogger(__name__)


class SaveHelperTest( unittest.TestCase ):

    def test_count_pageslips__good_multi(self):
        """ Tests count with good input & multiple pageslips printed. """
        counter = PageslipCounter()
        screen_text = 'jta_aug24_0840[16;6H[JPress <ESCAPE> to STOP printing[19;6H[KNow printing 1"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 2"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 3"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 4"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 5"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[19;6H[KNow printing 6"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[14;6H[JPrinting Complete[15;6H6 notices printed.[16;6HWas the printout OK? (y/n) '
        result = counter.count_pageslips( screen_text )
        self.assertEqual( unicode, type(result) )
        self.assertEqual( '6', result )

    def test_count_pageslips__good_single(self):
        """ Tests count with good input & single pageslips printed. """
        counter = PageslipCounter()
        screen_text = 'jta_aug25_0844[16;6H[JPress <ESCAPE> to STOP printing[19;6H[KNow printing 1"/iiidb/circ/holdshelfmap" is wrongly formatted on line 2 : ""[14;6H[JPrinting Complete[15;6H1 notice printed.[16;6HWas the printout OK? (y/n)'
        result = counter.count_pageslips( screen_text )
        self.assertEqual( unicode, type(result) )
        self.assertEqual( '1', result )

    def test_count_pageslips__bad(self):
        """ Tests count with bad input. """
        counter = PageslipCounter()
        screen_text = 'blah'
        result = counter.count_pageslips( screen_text )
        self.assertEqual( unicode, type(result) )
        self.assertEqual( '0', result )

    # end class SaveHelperTest


if __name__ == "__main__":
    unittest.main()
