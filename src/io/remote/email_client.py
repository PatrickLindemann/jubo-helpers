import imaplib
import smtplib
import ssl
import time
from typing import List

from src.model.config import Config, Server, User
from src.model.mail import Mail

class EmailClient:

    user: User
    servers: List[Server]
    imap: any
    smtp: any

    def __init__(self, config: Config):
        self.user = config.user
        self.servers = config.servers
        # Connect to the IMAP server
        try:
            self.imap = imaplib.IMAP4_SSL(self.servers['imap'].host, self.servers['imap'].port)
            self.imap.login(self.user.email, self.user.password)
        except Exception as e:
            self.close()
            raise e
        # Connect to the SMTP server
        try:
            context = ssl.create_default_context()
            self.smtp = smtplib.SMTP_SSL(self.servers['smtp'].host, self.servers['smtp'].port, context=context)
            self.smtp.login(self.user.email, self.user.password)
        except Exception as e:
            self.close()
            raise e

    def send(self, mail: Mail):
        self.smtp.sendmail(mail.sender, mail.recipients, mail.as_string())
        self.imap.append('Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), mail.as_string().encode('utf8'))

    def close(self):
        try:
            if self.smtp:
                self.smtp.logout()
                self.smtp.close()
        except:
            pass
        try:
            if self.imap:
                self.imap.logout()
                self.imap.close()
        except:
            pass