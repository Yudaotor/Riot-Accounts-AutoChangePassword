import email
from traceback import print_exc
import re
import imaplib


def setId(conn, username):
    """
    Sets the ID for the IMAP connection.

    Args:
        conn (imaplib.IMAP4): The IMAP connection object.
        username (str): The username for the ID.

    Returns:
        None
    """
    imaplib.Commands['ID'] = 'AUTH'
    args = ("name", username.split("@")[0], "contact", username, "version", "1.0.0", "vendor", username.split("@")[0]+"Client")
    conn._simple_command('ID', '("' + '" "'.join(args) + '")')


def fetchCode(self):
    """
    Fetches the verification code from the latest email.

    Returns:
        None
    """
    try:
        status, info = self.M.uid('search', None, 'ALL')
        if status == "OK":
            status, info = self.M.uid('fetch', info[0].split()[-1], '(RFC822)')
            if status == "OK":
                mail = email.message_from_bytes(info[0][1])
                if mail['From'].find('noreply@mail.accounts.riotgames.com') > -1:
                    self.code = re.findall(r'\d{6}', mail["Subject"])[0]
    except Exception:
        print_exc()


class IMAP(object):
    def __init__(self, conn, username):
        setId(conn, username)
        conn.select("INBOX")
        self.M = conn
        self.code = ""
        fetchCode(self)



