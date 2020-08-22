import logging
import smtplib
import sys
import traceback
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Set

from mail.recipient import Recipient
from utility.parse import date_to_string, text_to_html
from utility.timeout import timeout_limit


class Sender:

    def __init__(self, smtp_server: str, port: int, email_address: str,
                 password: str):
        self.server = smtplib.SMTP_SSL(smtp_server, port)
        self.server.ehlo()
        self.email_address = email_address
        self.server.login(email_address, password)

    def send_email(self, subject: str, recipients: Set[str], body_html: str):
        logging.info(f"Sending from {self.email_address}, to {recipients}")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.email_address
        message["To"] = ", ".join(recipients)
        message.attach(MIMEText(body_html, "html"))
        self.server.sendmail(self.email_address, list(recipients),
                             message.as_string())

    def send_recipient_email(self, recipient: Recipient, retry: int = 0,
                             timeout_seconds: int = 60,
                             send_self: bool = False,
                             test_next_day: bool = False):
        destination_email_address = {recipient.email_address}
        if send_self:
            destination_email_address.add(self.email_address)
        try:
            with timeout_limit(timeout_seconds):
                subject = recipient.generate_subject()
                body_html = recipient.generate_body()
                self.send_email(subject, destination_email_address, body_html)
                logging.info(f"Email sent to {recipient.email_address}")
        except Exception as exception:
            logging.info(
                    f"Exception occured during body generation: {exception}")
            if retry > 0:
                logging.info(f"Retrying with remaining tries of {retry}")
                self.send_recipient_email(recipient, retry - 1, timeout_seconds,
                                          send_self, test_next_day)
            else:
                logging.info("No more retires")
                self.send_exception(
                        f"BotDaily - CURRENT_DAY EXCEPTION for {date_to_string(recipient.current_date_time)}",
                        recipient, exception)
                logging.info("Exception Email sent to sender.")

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
            with timeout_limit(timeout_seconds):
                recipient_next_day.generate_subject()
                recipient_next_day.generate_body()
                logging.info(
                        f"Checked for {recipient.email_address} on {date_to_string(next_day_date_time)}")
        except Exception as exception:
            logging.info(exception)
            self.send_exception(
                    f"BotDaily - NextDay Exception for {date_to_string(next_day_date_time)}",
                    recipient, exception)

    def send_exception(self, subject: str, recipient: Recipient,
                       exception: Exception):
        logging.info(f"Sending exception")
        self.send_email(subject, {self.email_address},
                        text_to_html(f"""Recipient: {recipient.email_address}


Exception: {exception}


Traceback: {traceback.format_exc()}


System Information: {sys.exc_info()[2]}
"""))


class GmailSender(Sender):

    def __init__(self, email_address: str, password: str):
        super().__init__("smtp.gmail.com", 465, email_address, password)
