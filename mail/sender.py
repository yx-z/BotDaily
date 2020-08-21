import logging
import smtplib
import sys
import traceback
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import List

from mail.recipient import Recipient
from utility.parse import date_to_string
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

    def send_email(self, subject: str, recipients: List[str], body_html: str,
                   retry: int = 0, timeout_seconds: int = 60):
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
                self.send_email(subject, recipients, body_html, retry - 1,
                                timeout_seconds)
            else:
                raise exception

    def send_recipient_email(self, recipient: Recipient, retry: int = 0,
                             timeout_seconds: int = 60,
                             send_self: bool = True,
                             test_next_day: bool = True):
        destination_email_addresses = [recipient.email_address]
        if send_self:
            destination_email_addresses.append(self.email_address)
        try:
            self.send_email(recipient.generate_subject(),
                            destination_email_addresses,
                            recipient.generate_body(), retry,
                            timeout_seconds)
        except Exception as exception:
            logging.info(exception)
            self.send_exception(
                    f"BotDaily - !CURRENT_DAY EXCEPTION! for {date_to_string(recipient.current_date_time)}",
                    recipient, exception)

        if test_next_day:
            self.test_recipient_next_day(recipient, timeout_seconds)

    def test_recipient_next_day(self, recipient: Recipient,
                                timeout_seconds: int):
        next_day_date_time = recipient.current_date_time + timedelta(days=1)
        recipient_next_day = recipient.copy()
        recipient_next_day.subject.current_date_time = next_day_date_time
        for feature in recipient.features:
            feature.current_date_time = next_day_date_time
        try:
            with timeout(timeout_seconds):
                recipient_next_day.generate_subject()
                recipient_next_day.generate_body()
        except Exception as exception:
            logging.info(exception)
            self.send_exception(
                    f"BotDaily - NextDay Exception for {date_to_string(next_day_date_time)}",
                    recipient, exception)

    def send_exception(self, subject: str, recipient: Recipient,
                       exception: Exception):
        self.send_email(subject, [self.email_address],
                        f"""Recipient: {recipient}

Exception: {exception}

Traceback: {traceback.format_exc()}

System Information: {sys.exc_info()[2]}
""")

    def close(self):
        self.server.close()


class GmailSender(Sender):

    def __init__(self, email_address: str, password: str):
        super().__init__("smtp.gmail.com", 465, email_address, password)
