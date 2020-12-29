import logging
import os
import sys
import time
from math import ceil

from configuration.secret import LOG_DIR, SENDER_EMAIL, SENDER_PASSWORD
from mail.sender import GmailSender
from utility.constant import *
from datetime import datetime, timedelta
from mail.recipient import Recipient
from mail.subject import Subject
from feature import *
from utility.logger import setup_prod_logger, setup_test_logger
from utility.system import process_exists, sleep_until_next_minute
from typing import List, Dict

NUM_RETRY = 2
SEND_SELF = True
ALSO_TEST_NEXT = True


def main(args):
    if not process_exists("node"):
        os.system("node netease-api/app.js &")

    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)

    is_prod = len(args) == 1
    if is_prod:
        if process_exists("python"):
            logging.warning("BotDaily process already exists.")
            return
        while True:
            now = datetime.now()
            setup_prod_logger(now)
            now_str = now.strftime("%H:%M")
            time_to_recipients = get_recipients()
            if now_str in time_to_recipients:
                for recipient in time_to_recipients[now_str]:
                    recipient.set_current_date_time(now)
                    sender.send_recipient_email(
                        recipient,
                        send_self=SEND_SELF,
                        num_retry=NUM_RETRY,
                        also_test_next=ALSO_TEST_NEXT,
                    )
            elif now.minute == 0:
                logging.info("Sleeping.")

            sleep_until_next_minute(now)
    else:
        now = datetime.now()
        setup_test_logger(now)
        mode = args[1]
        if mode.startswith("test"):

            def test_recipient(recipient: Recipient):
                set_recipient_test_mode(recipient, now, args)
                if mode == "test":
                    sender.send_recipient_email(
                        recipient, also_test_next=ALSO_TEST_NEXT
                    )
                elif mode == "testNext":
                    sender.test_recipient_next_day(recipient)

            for_all_recipients(test_recipient)
        elif mode.startswith("now"):

            def send_recipient_now(recipient: Recipient):
                recipient.set_current_date_time(now)
                sender.send_recipient_email(
                    recipient,
                    send_self=SEND_SELF,
                    num_retry=NUM_RETRY,
                    also_test_next=ALSO_TEST_NEXT,
                )

            for_all_recipients(send_recipient_now)


def set_recipient_test_mode(recipient: Recipient, date: datetime, args: List[str]):
    recipient.email_address = SENDER_EMAIL
    recipient.on_email_sent = lambda: None
    recipient.set_current_date_time(date)
    previous_subject = recipient.generate_subject
    recipient.generate_subject = lambda: f"TEST {previous_subject()}"
    if len(args) > 2:
        recipient.test_next_day_feature = args[2:]


def get_recipients() -> Dict[str, List[Recipient]]:
    with open("configuration/recipient.py", "r") as file:
        return eval(file.read())


def for_all_recipients(recipient_action):
    for _, recipients in get_recipients().items():
        for recipient in recipients:
            recipient_action(recipient)


if __name__ == "__main__":
    main(sys.argv)
