import imaplib
import smtplib
import ssl
import time
from typing import Optional, TypedDict
from dataclasses import dataclass

from src.model.mail import Mail

class ServerConfig(TypedDict):
    host: str
    port: int
    user: str
    password: str

class EmailClientWithSSLConfig(TypedDict):
    imap: ServerConfig
    smtp: ServerConfig

class EmailClientWithSSLConnections(TypedDict):
    imap: Optional[imaplib.IMAP4_SSL]
    smtp: Optional[smtplib.SMTP_SSL]

class EmailClientWithSSL:
    config: EmailClientWithSSLConfig
    connections: EmailClientWithSSLConnections

    def __init__(self, imap: ServerConfig, smtp: ServerConfig):
        self.config = { 'imap': imap, 'smtp': smtp }
        self.connections = {}

    def test_imap(self) -> bool:
        con = self.__get_imap_connection()
        return con.check()
    
    def test_smtp(self) -> bool:
        con = self.__get_smtp_connection()
        return con.check()

    def connect(self):
        self.__get_imap_connection()
        self.__get_smtp_connection()

    def send(self, mail: Mail):
        imap = self.__get_imap_connection()
        smtp = self.__get_smtp_connection()
        smtp.sendmail(mail.sender, mail.recipients, mail.as_string())
        imap.append('Sent', '\\Seen', imaplib.Time2Internaldate(time.time()), mail.as_string().encode('utf8'))

    def close(self):
        for con in self.connections.values():
            try:
                con.close()
            except:
                pass

    def __get_imap_connection(self) -> imaplib.IMAP4_SSL:
        if 'imap' in self.connections:
            return self.connections['imap']
        con = imaplib.IMAP4_SSL(self.config['imap']['host'], self.config['imap']['port'])
        try:
            con.login(self.config['imap']['user'], self.config['imap']['password'])
        except Exception as ex:
            con.close()
            raise ex
        return con

    def __get_smtp_connection(self) -> smtplib.SMTP_SSL:
        if 'smtp' in self.connections:
            return self.connections['smtp']
        con = smtplib.SMTP_SSL(
            self.config['smtp']['host'],
            self.config['smtp']['port'],
            context = ssl.create_default_context()
        )
        try:
            con.login(self.config['smtp']['user'], self.config['smtp']['password'])
        except Exception as ex:
            con.close()
            raise ex
        return con