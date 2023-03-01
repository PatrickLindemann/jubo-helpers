from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List, Union


@dataclass
class Mail:
    
    sender: str
    recipients: Union[str, List[str]]
    subject: str
    body: str

    def as_message(self):
        message = MIMEMultipart()
        message["From"] = self.sender
        message["To"] = self.recipients
        message["Subject"] = self.subject
        message.attach(MIMEText(self.body, "html"))
        return message

    def as_string(self):
        return self.as_message().as_string()