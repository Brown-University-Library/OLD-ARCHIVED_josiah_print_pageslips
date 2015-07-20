"""
Part of Josiah-to-Las_Josiah code.
"""

from __future__ import unicode_literals

import unittest
from josiah_print_pageslips.classes import NumberDeterminer


class NumberDeterminerTest(unittest.TestCase):



	def testDetermineFileNumber_goodInput_fileNameA(self):
		"""determines the integer representing a file to FTP to sulu"""

		determinerInstance = NumberDeterminer.NumberDeterminer()

		textOfScreen = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > jta_20060328_170905.p[4;1H2 > blahFile.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'
#		fileName = 'jta_sep01_0947'

		expected = str(1)
		returned = determinerInstance.determineFileNumber(textOfScreen)
		self.assertEqual( expected, returned, "returned is: " + str(returned) )

		expected = "jta_20060328_170905.p"
		returned = determinerInstance.foundFileName
		self.assertEqual( expected, returned, "returned is: " + str(returned) )



	def testDetermineFileNumber_noFileFound(self):
		"""determines the integer representing a file to FTP to sulu"""

		determinerInstance = NumberDeterminer.NumberDeterminer()

		textOfScreen = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > blahFile_A.p[4;1H2 > blahFile_B.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'
#		fileName = 'jta_sep01_0947'

		expected = "-1"
		returned = determinerInstance.determineFileNumber(textOfScreen)
		self.assertEqual( expected, returned, "returned is: " + str(returned) )

		expected = ""
		returned = determinerInstance.foundFileName
		self.assertEqual( expected, returned, "returned is: " + str(returned) )



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



	def testDetermineFileCount(self):
		"""determine count of files in 'files to ftp' list"""

		determinerInstance = NumberDeterminer.NumberDeterminer()
		screenText = '[21;57H[4h [4lf[21;58H[1;1H[K[2;1H[K[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;18H        Loading program you requested[K[14;1H[K[15;1H[K[16;1H[K[17;1H[K[18;1H[K[19;1H[K[20;1H[K[21;1H[K[22;1H[K[14;41H[H[2J[1;20HSend print files out of INNOPAC using FTP[3;1H[K[4;1H[K[5;1H[K[6;1H[K[7;1H[K[8;1H[K[9;1H[K[10;1H[K[11;1H[K[12;1H[K[13;1H[K[14;1H[K[15;1H[K[3;1H1 > blahFile_A.p[4;1H2 > blahFile_B.p[5;1H3 > test.p[16;1H[K(0lqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqk[17;1H[Kx(BF > FTP a print file to another system[17;79H(0x[18;1H[Kx(BR > REMOVE files[18;79H(0x[19;1H[Kx(BY > DISPLAY file SIZE & DATE[19;79H(0x[20;1H[Kx(BQ > QUIT[20;79H(0x[21;1H[Kx(BChoose one (F,R,Y,Q)[21;79H(0x[22;1H[Kx[22;79Hx[23;1H[Kx[23;79Hx[24;1H[Kmqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqqj(B[21;23H[?1l>[21;23H'

		expected = 3
		returned = determinerInstance.determineFileCount(screenText)
		self.assertEqual( expected, returned, "returned is: " + str(returned) )



if __name__ == "__main__":
	unittest.main()
