# -*- coding: utf-8 -*-

"""
Tests josiah_print_pageslips.classes.TransferHelper
"""

from __future__ import unicode_literals

import logging, os, unittest
from josiah_print_pageslips.classes.TransferHelper import FileNumberGrabber, FileCounter


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


class FileNumberGrabberTest( unittest.TestCase ):

    def test_grab_file_number__found_input(self):
        """ Tests file-number and file-name grab from data containing a target filename. """
        grabber = FileNumberGrabber()
        screen_text = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > jta_20060328_170905.p[4;1H2 > blahFile.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'
        result = grabber.grab_file_number( screen_text )
        self.assertEqual( unicode, type(result) )
        self.assertEqual( '1', result )
        self.assertEqual( 'jta_20060328_170905.p', grabber.found_file_name )

    def test_grab_file_number__good_input(self):
        """ Tests file-number and file-name grab from data containing _no_ target filename. """
        grabber = FileNumberGrabber()
        screen_text = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > blahFile_A.p[4;1H2 > blahFile_B.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'
        result = grabber.grab_file_number( screen_text )
        self.assertEqual( unicode, type(result) )
        self.assertEqual( '-1', result )
        self.assertEqual( '', grabber.found_file_name )

    # end class FileNumberGrabberTest


class FileCounterTest( unittest.TestCase ):

    def test_count_ftp_files(self):
        """ Tests number of files in ftp list. """
        counter = FileCounter()
        screen_text = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > blahFile_A.p[4;1H2 > blahFile_B.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'
        result = counter.count_ftp_list_files( screen_text )
        self.assertEqual( int, type(result) )
        self.assertEqual( 3, result )

    # end class FileCounterTest


if __name__ == "__main__":
    unittest.main()
