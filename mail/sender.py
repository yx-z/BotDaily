import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from mail.recipient import Recipient
from utility.timeout import timeout


class Sender:

    def __init__(self, smtp_server: str, port: int, email_address: str,
                 password: str):
        try:
            self.server = smtplib.SMTP_SSL(smtp_server, port)
            self.server.ehlo()

            self.email_address = email_address
            self.server.login(email_address, password)
        except Exception as exception:
            raise exception

    def send_message(self, subject: str, recipients: List[str], body_html: str,
                     retry: int, timeout_seconds: int):
        try:
            with timeout(timeout_seconds):
                message = MIMEMultipart("alternative")
                message["Subject"] = subject
                message["From"] = self.email_address
                message["To"] = ", ".join(recipients)
                message.attach(MIMEText(body_html, "html"))
                self.server.sendmail(self.email_address, recipients,
                                     message.as_string())
        except Exception as exception:
            if retry > 0:
                self.send_message(subject, recipients, body_html, retry - 1,
                                  timeout_seconds)
            else:
                raise exception

    def send_recipient_message(self, recipient: Recipient, retry: int = 0,
                               timeout_seconds: int = 60,
                               send_self: bool = True):
        destination_email_addresses = [recipient.email_address]
        if send_self:
            destination_email_addresses.append(self.email_address)
        self.send_message(recipient.generate_subject(),
                          destination_email_addresses,
                          recipient.generate_body(), retry,
                          timeout_seconds)

    def close(self):
        self.server.close()


class GmailSender(Sender):

    def __init__(self, email_address: str, password: str):
        super().__init__("smtp.gmail.com", 465, email_address, password)
