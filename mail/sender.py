import logging
import smtplib
import traceback
from datetime import timedelta
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Set

from mail.recipient import Recipient
from utility.constant import SECONDS_IN_MINUTE
from utility.html_builder import html_from_text
from utility.parse import date_to_string
from utility.system import timeout_limit


class Sender:
    def __init__(self, email_address: str, password: str, smtp_server: str, port: int):
        self.smtp_server = smtp_server
        self.port = port
        self.email_address = email_address
        self.password = password

    def send_recipient_email(
        self,
        recipient: Recipient,
        num_retry: int = 0,
        timeout_seconds: int = SECONDS_IN_MINUTE,
        send_self: bool = False,
        also_test_next: bool = False,
    ):
        destination_email_address = {recipient.email_address}
        if send_self:
            destination_email_address.add(self.email_address)
        try:
            with timeout_limit(timeout_seconds):
                subject = recipient.generate_subject()
                body_html = recipient.generate_body(test_filter=False)
                logging.info(body_html)
                self._send_email(subject, destination_email_address, body_html)
                logging.info(f"Email sent to {destination_email_address}")
                recipient.on_email_sent()
        except Exception as exception:
            logging.info(f"Exception occured during body generation: {exception}")
            logging.info(traceback.format_exc())
            if num_retry > 0:
                logging.info(f"Retrying with remaining tries of {num_retry}")
                self.send_recipient_email(
                    recipient, num_retry - 1, timeout_seconds, send_self
                )
            else:
                logging.info("No more retires")
                self.send_exception(
                    f"BotDaily - CURRENT_DAY EXCEPTION for {date_to_string(recipient.current_date_time)}",
                    recipient,
                    exception,
                )
                logging.info("Exception Email sent to sender.")

        if also_test_next and len(recipient.test_next_day_feature) > 0:
            self.test_recipient_next_day(recipient, timeout_seconds)

    def test_recipient_next_day(
        self, recipient: Recipient, timeout_seconds: int = SECONDS_IN_MINUTE
    ):
        current_date_time = recipient.current_date_time
        next_day_date_time = current_date_time + timedelta(days=1)
        next_day_date_time_string = date_to_string(next_day_date_time)
        logging.info(
            f"Checking for {recipient.email_address} on {next_day_date_time_string}"
        )
        recipient.set_current_date_time(next_day_date_time)
        try:
            with timeout_limit(timeout_seconds):
                subject = recipient.generate_subject()
                body_html = recipient.generate_body(test_filter=True)
                logging.info(
                    f"Checked for {recipient.email_address} on {next_day_date_time_string}"
                )
                self._send_email(
                    f"NextDay {subject} for {recipient.email_address} on {next_day_date_time_string}",
                    {self.email_address},
                    body_html,
                )
        except Exception as exception:
            logging.info(exception)
            self.send_exception(
                f"BotDaily - NextDay Exception for {next_day_date_time_string}",
                recipient,
                exception,
            )
        finally:
            recipient.set_current_date_time(current_date_time)

    def send_exception(self, subject: str, recipient: Recipient, exception: Exception):
        logging.info(f"Sending exception")
        self._send_email(
            subject,
            {self.email_address},
            html_from_text(
                f"""Recipient: {recipient.email_address}
                
Exception: {exception}

Traceback: {traceback.format_exc()}
"""
            ),
        )

    def _send_email(self, subject: str, recipients: Set[str], body_html: str):
        logging.info(f"Sending from {self.email_address} to {recipients}")
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.email_address
        message["To"] = ", ".join(recipients)
        message.attach(MIMEText(body_html, "html"))

        server = smtplib.SMTP_SSL(self.smtp_server, self.port)
        server.ehlo()
        server.login(self.email_address, self.password)
        server.sendmail(self.email_address, list(recipients), message.as_string())
        server.close()


class GmailSender(Sender):
    def __init__(
        self,
        email_address: str,
        password: str,
        smtp_server: str = "smtp.gmail.com",
        port: int = 465,
    ):
        super().__init__(email_address, password, smtp_server, port)
