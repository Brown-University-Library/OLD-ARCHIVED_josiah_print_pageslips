# -*- coding: utf-8 -*-

""" Unicode-friendly emailer.
    Called by both FileSaveController.py and FileTransferController.py """

from __future__ import unicode_literals

import json, logging, os, pprint, smtplib
from email.Header import Header
from email.mime.text import MIMEText


log = logging.getLogger(__name__)


class Mailer( object ):
    """ Specs email handling. """

    def __init__( self, UNICODE_SUBJECT, UNICODE_MESSAGE ):
        self.UTF8_SMTP_SERVER = os.environ['PGSLP__UTF8_SMTP_SERVER']
        self.UTF8_RAW_TO_JSON = os.environ['PGSLP__UTF8_RAW_TO_JSON']  # json (ensures reliable formatting/encoding), eg: '["addr1@domain.edu", "addr2@domain.com"]'
        self.UTF8_FROM_REAL = os.environ['PGSLP__UTF8_FROM_REAL']  # real 'from' address smtp server will user, eg: 'addr3@domain.edu'
        self.UTF8_FROM_HEADER = os.environ['PGSLP__UTF8_FROM_HEADER']  # apparent 'from' string user will see, eg: 'some_system'
        self.UTF8_REPLY_TO_HEADER = os.environ['PGSLP__UTF8_REPLY_TO_HEADER']
        self.UNICODE_SUBJECT = UNICODE_SUBJECT
        self.UNICODE_MESSAGE = UNICODE_MESSAGE
        log.debug( 'Mailer instantiated' )

    def send_email( self ):
        """ Sends email. """
        try:
            TO = self._build_mail_to()  # list of utf-8 entries
            MESSAGE = self.UNICODE_MESSAGE.encode( 'utf-8', 'replace' )  # utf-8
            payload = self._assemble_payload( TO, MESSAGE )
            s = smtplib.SMTP( self.UTF8_SMTP_SERVER )
            s.sendmail( self.UTF8_FROM_REAL, TO, payload.as_string() )
            s.quit()
            log.debug( 'mail sent' )
            return True
        except Exception as e:
            log.error( 'problem sending mail, exception, `%s`' % unicode(repr(e)) )
            return False

    def _build_mail_to( self ):
        """ Builds and returns 'to' list of email addresses.
            Called by send_email() """
        to_emails = json.loads( self.UTF8_RAW_TO_JSON )
        utf8_to_list = []
        for address in to_emails:
            utf8_to_list.append( address.encode('utf-8') )
        return utf8_to_list

    def _assemble_payload( self, TO, MESSAGE ):
        """ Puts together and returns email payload.
            Called by send_email(). """
        payload = MIMEText( MESSAGE )
        payload['To'] = ', '.join( TO )
        payload['From'] = self.UTF8_FROM_HEADER
        payload['Subject'] = Header( self.UNICODE_SUBJECT, 'utf-8' )  # SUBJECT must be unicode
        payload['Reply-to'] = self.UTF8_REPLY_TO_HEADER
        return payload

    # end class Mailer
