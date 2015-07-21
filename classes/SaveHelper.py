# -*- coding: utf-8 -*-

"""
Helpers for FileSaveController.py
"""

from __future__ import unicode_literals

import logging


log = logging.getLogger(__name__)


class SaveHelper( object ):

    def count_pageslips( self, screen_text ):
        """ Returns count of pageslips printed.
            Called by FileSaveController.run_code() """
        notices_position = self._find_notices_segment( screen_text )
        if not notices_position:
            return '0'
        segment = screen_text[ notices_position-10: notices_position ]
        initial_position = segment.find( '[15;6H' )
        count_string_start = initial_position + 6
        count_string = segment[ count_string_start: ]
        log.debug( 'count_string, `%s`' % count_string )
        return count_string

    def _find_notices_segment( self, screen_text ):
        """ Returns position of " notices printed." or " notice printed."
            Called by count_pageslips() """
        notices_position = screen_text.find( ' notices printed' )
        if notices_position == -1:
            notices_position = screen_text.find( ' notice printed' )
        if notices_position == -1:
            return False
        else:
            return notices_position

    # end class SaveHelper
