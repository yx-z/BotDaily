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
from utility.system import process_exists

if __name__ == '__main__':
    if not process_exists("node"):
        os.system("node netease-api/app.js &")
    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    args = sys.argv
    if len(args) > 1 and args[1].startswith("test"):
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

        time_to_recipients = eval(
            open("configuration/recipient.py", "r").read())
        for _, recipients in time_to_recipients.items():
            for recipient in recipients:
                recipient.email_address = SENDER_EMAIL
                recipient.on_email_sent = lambda: None
                recipient.set_current_date_time(datetime.now())

                if args[1] == "test":
                    is_test = len(args) > 2
                    if is_test:
                        recipient.is_test = args[2:]
                    sender.send_recipient_email(recipient,
                                                test_next_day=is_test)
                elif args[1] == "testNext":
                    if len(args) > 2:
                        recipient.is_test = args[2:]
                    sender.test_recipient_next_day(recipient)
    elif len(args) == 0:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename=LOG_FILE)
        logging.info(f"PID - {os.getpid()}")

        while True:
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            time_to_recipients = eval(
                open("configuration/recipient.py", "r").read())
            if now_str in time_to_recipients.keys():
                for recipient in time_to_recipients[now_str]:
                    recipient.set_current_date_time(now)
                    sender.send_recipient_email(recipient, send_self=True,
                                                test_next_day=True)
            elif now.minute == 0:
                logging.info("Sleeping.")
            next_minute = datetime(now.year, now.month, now.day, now.hour,
                                   now.minute) + timedelta(minutes=1)
            sleep_time = max(0, ceil(
                (next_minute - datetime.now()).total_seconds()))
            time.sleep(sleep_time)
