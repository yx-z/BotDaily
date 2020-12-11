import logging
import os
import sys
import time
from math import ceil

from configuration.secret import LOG_FILE, SENDER_EMAIL, SENDER_PASSWORD
from mail.sender import GmailSender
from utility.constant import *
from datetime import datetime, timedelta
from mail.recipient import Recipient
from mail.subject import Subject
from feature import *
from utility.logger import setup_prod_logger, setup_test_logger
from utility.system import process_exists
from typing import List, Dict


def main(args):
    if not process_exists("node"):
        os.system("node netease-api/app.js &")

    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)

    is_prod = len(args) == 1
    if is_prod:
        if process_exists("python3 main.py"):
            logging.warning("BotDaily process already exists.")
            return
        setup_prod_logger()
        while True:
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            time_to_recipients = get_recipients()
            if now_str in time_to_recipients:
                for recipient in time_to_recipients[now_str]:
                    recipient.set_current_date_time(now)
                    sender.send_recipient_email(
                        recipient, send_self=True, num_retry=2, also_test_next=True
                    )
            elif now.minute == 0:
                logging.info("Sleeping.")

            sleep_until_next_minute(now)
    else:
        setup_test_logger()
        mode = args[1]
        if mode.startswith("test"):

            def test_recipient(recipient: Recipient):
                setup_recipient_test_mode(recipient, args)
                if mode == "test":
                    sender.send_recipient_email(recipient, also_test_next=True)
                elif mode == "testNext":
                    sender.test_recipient_next_day(recipient)

            for_all_recipients(test_recipient)
        elif mode.startswith("now"):

            def send_recipient_now(recipient: Recipient):
                recipient.set_current_date_time(datetime.now())
                sender.send_recipient_email(
                    recipient, send_self=True, num_retry=2, also_test_next=True
                )

            for_all_recipients(send_recipient_now)


def setup_recipient_test_mode(recipient: Recipient, args: List[str]):
    recipient.email_address = SENDER_EMAIL
    recipient.on_email_sent = lambda: None
    recipient.set_current_date_time(datetime.now())
    previous_subject = recipient.generate_subject
    recipient.generate_subject = lambda: f"TEST {previous_subject()}"
    if len(args) > 2:
        recipient.test_next_day_feature = args[2:]


def get_recipients() -> Dict[str, List[Recipient]]:
    return eval(open("configuration/recipient.py", "r").read())


def for_all_recipients(recipient_action):
    for _, recipients in get_recipients().items():
        for recipient in recipients:
            recipient_action(recipient)


def sleep_until_next_minute(now: datetime):
    next_minute = datetime(
        now.year, now.month, now.day, now.hour, now.minute
    ) + timedelta(minutes=1)
    sleep_time = max(0, ceil((next_minute - datetime.now()).total_seconds()))
    time.sleep(sleep_time)


if __name__ == "__main__":
    main(sys.argv)
