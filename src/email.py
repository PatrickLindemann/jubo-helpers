import imaplib
import os
import pathlib
import smtplib
import ssl
import time
from dataclasses import dataclass
from email.message import EmailMessage
from typing import List, Optional

import dotenv

from .paths import ROOT_DIR


class Attachment:
    file_path: pathlib.Path
    mime_type: str
    name: str

    def __init__(
        self, file_path: pathlib.Path, mime_type: str, name: Optional[str] = None
    ):
        self.file_path = file_path
        assert os.path.isfile(
            file_path
        ), f'Attachment file does not exist: "{file_path}"'
        self.mime_type = mime_type
        assert (
            len(mime_type.split("/")) == 2
        ), f'Invalid mime type: "{mime_type}". Expected "<maintype>/<subtype>".'
        self.name = name if name else file_path.name

    @property
    def mime_maintype(self) -> str:
        return self.mime_type.split("/")[0]

    @property
    def mime_subtype(self) -> str:
        return self.mime_type.split("/")[1]


@dataclass
class Email:
    sender: str
    to: List[str]
    subject: str
    content: str
    cc: Optional[List[str]] = None
    bcc: Optional[List[str]] = None
    attachments: Optional[List[Attachment]] = None

    def as_message(self) -> EmailMessage:
        message = EmailMessage()
        message["From"] = self.sender
        message["To"] = ", ".join(self.to)
        if self.cc:
            message["Cc"] = ", ".join(self.cc)
        if self.bcc:
            message["Bcc"] = ", ".join(self.bcc)
        message["Subject"] = self.subject
        message.set_content(self.content, subtype="html")
        if self.attachments:
            for attachment in self.attachments:
                with open(attachment.file_path, "rb") as file:
                    message.add_attachment(
                        file.read(),
                        maintype=attachment.mime_maintype,
                        subtype=attachment.mime_subtype,
                        filename=attachment.name,
                    )
        return message

    def __str__(self) -> str:
        return self.as_message().as_string()


@dataclass
class EmailSignatureConfig:

    name: str
    role: str
    email: str
    phone: str

    @staticmethod
    def from_dotenv(
        file_path: pathlib.Path = ROOT_DIR / ".env",
    ) -> "EmailSignatureConfig":
        assert (
            file_path.exists()
        ), f'Environment file does not exist: "{file_path.resolve()}".'
        values = dotenv.dotenv_values(file_path)
        return EmailSignatureConfig(
            name=values["SIGNATURE_NAME"],
            role=values["SIGNATURE_ROLE"],
            email=values["SIGNATURE_EMAIL"],
            phone=values["SIGNATURE_PHONE"],
        )


@dataclass
class EmailClientConfig:

    user: str
    password: str
    imap_host: str
    imap_port: int
    smtp_host: str
    smtp_port: int

    @staticmethod
    def from_dotenv(file_path: pathlib.Path = ROOT_DIR / ".env") -> "EmailClientConfig":
        assert (
            file_path.exists()
        ), f'Environment file does not exist: "{file_path.resolve()}".'
        values = dotenv.dotenv_values(file_path)
        return EmailClientConfig(
            user=values["EMAIL_USER"],
            password=values["EMAIL_PASSWORD"],
            imap_host=values["EMAIL_IMAP_HOST"],
            imap_port=int(values["EMAIL_IMAP_PORT"]),
            smtp_host=values["EMAIL_SMTP_HOST"],
            smtp_port=int(values["EMAIL_SMTP_PORT"]),
        )


class EmailClient:
    _imap = imaplib.IMAP4_SSL
    _smtp = smtplib.SMTP_SSL

    def __init__(
        self,
        user: str,
        password: str,
        imap_host: str,
        imap_port: int,
        smtp_host: str,
        smtp_port: int,
    ) -> None:
        # Connect to the IMAP server with SSL
        try:
            self._imap = imaplib.IMAP4_SSL(imap_host, imap_port)
            self._imap.login(user, password)
        except Exception as ex:
            self.close()
            raise ex
        # Connect to the SMTP server with SSL
        try:
            self._smtp = smtplib.SMTP_SSL(
                smtp_host, smtp_port, context=ssl.create_default_context()
            )
            self._smtp.login(user, password)
        except:
            self.close()
            raise ex

    def send(self, email: Email) -> None:
        self._smtp.sendmail(from_addr=email.sender, to_addrs=email.to, msg=str(email))
        self._imap.append(
            mailbox="Sent",
            flags="\\Seen",
            date_time=imaplib.Time2Internaldate(time.time()),
            message=str(email).encode("utf8"),
        )

    def draft(self, email: Email) -> None:
        self._imap.append(
            mailbox="Drafts",
            flags="\\Draft",
            date_time=imaplib.Time2Internaldate(time.time()),
            message=str(email).encode("utf8"),
        )

    def close(self) -> None:
        if self._imap:
            try:
                self._imap.close()
            except:
                pass
        if self._smtp:
            try:
                self._smtp.close()
            except:
                pass
