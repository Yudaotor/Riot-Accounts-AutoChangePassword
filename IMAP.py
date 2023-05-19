import email
import traceback
from threading import *
from datetime import datetime
import re
import imaplib


def setId(conn, username):
    imaplib.Commands['ID'] = 'AUTH'
    args = ("name", username.split("@")[0], "contact", username, "version", "1.0.0", "vendor", username.split("@")[0]+"Client")
    conn._simple_command('ID', '("' + '" "'.join(args) + '")')


def fetchCode(self):
    try:
        status, info = self.M.uid('search', None, 'ALL')
        if status == "OK":
            status, info = self.M.uid('fetch', info[0].split()[-1], '(RFC822)')
            if status == "OK":
                mail = email.message_from_bytes(info[0][1])
                if mail['From'].find('noreply@mail.accounts.riotgames.com') > -1:
                    self.code = re.findall(r'\d{6}', mail["Subject"])[0]
    except Exception:
        traceback.print_exc()


class IMAP(object):
    def __init__(self, conn, username):
        setId(conn, username)
        conn.select("INBOX")
        self.M = conn
        self.code = ""
        fetchCode(self)



