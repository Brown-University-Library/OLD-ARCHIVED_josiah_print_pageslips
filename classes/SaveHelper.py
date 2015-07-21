# -*- coding: utf-8 -*-

"""
Helpers for FileSaveController.py
"""

from __future__ import unicode_literals

import json, logging, os, pprint, sys


class SaveHelper( object ):

    def count_pageslips(self, screenText):

        # issue: key screenText substring can be *either* 'notices' or 'notice.

        import string

        returnVal = "init"

        # find position of ' notices printed.' text, *or* ' notice printed.' text.
        foundPosition = "init"
        noticesPosition = string.find( screenText, " notices printed." ) # haystack, needle. Will be -1 if not found
        noticePosition = string.find( screenText, " notice printed." ) # haystack, needle. Will be -1 if not found

        if(noticesPosition > -1):
            foundPosition = noticesPosition
        else:
            if(noticePosition > -1):
                foundPosition = noticePosition

        if(foundPosition != "init"):
            # backup 10 spaces (too much, but no problem), and create a 10-character segment.
            segment1start = foundPosition - 10
            segment1end = foundPosition
            segment1 = screenText[segment1start:segment1end]

            # find the start position of the text '[15;6H' and reduce the sement to start after the 'H'. This is our number.
            foundPosition2 = string.find(segment1, "[15;6H")

            if(foundPosition > -1):
                segment2start = foundPosition2 + 6
                segment2 = segment1[segment2start:]
                returnVal = segment2
                if( returnVal == "1" ):
                    self.noticesPrintedText = "1 notice printed"
                else:
                    self.noticesPrintedText = returnVal + " notices printed"
            else:
                returnVal = "noNumFound"

        else:
            returnVal = "noNumFound"

        return returnVal

    # end class SaveHelper
