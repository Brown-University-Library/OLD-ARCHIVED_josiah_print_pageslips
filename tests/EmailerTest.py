# -*- coding: utf-8 -*-

"""
Tests josiah_print_pageslips.classes.Emailer
"""

from __future__ import unicode_literals

import logging, os, unittest
from josiah_print_pageslips.classes import Emailer


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


class EmailerTest( unittest.TestCase ):

    def testSendEmail_simple_text(self):
        """ Tests send with basic text. (Really sends!) """
        subject = 'test subject'
        message = 'test message'
        self.assertEqual( unicode, type(subject) )
        self.assertEqual( unicode, type(message) )
        emailerInstance = Emailer.Mailer( subject, message )
        self.assertEqual( True, emailerInstance.send_email() )

    def testSendEmail_unicode_text(self):
        """ Tests send with complex unicode subject and message. (Really sends!) """
        subject = 'tést_subject'
        message = '“test iñtërnâtiônàlĭzætiøn”'
        self.assertEqual( unicode, type(subject) )
        self.assertEqual( unicode, type(message) )
        emailerInstance = Emailer.Mailer( subject, message )
        self.assertEqual( True, emailerInstance.send_email() )


if __name__ == "__main__":
    unittest.main()
