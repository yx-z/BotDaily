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

if __name__ == '__main__':
    os.system("node netease-api/app.js &")
    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    if len(sys.argv) > 1 and sys.argv[1].startswith("test"):
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
                if sys.argv[1] == "test":
                    test_next_day = len(sys.argv) > 2
                    if test_next_day:
                        recipient.test_next_day = sys.argv[2:]
                    sender.send_recipient_email(recipient,
                                                test_next_day=test_next_day)
                elif sys.argv[1] == "testNext":
                    recipient.test_next_day = sys.argv[2:]
                    sender.test_recipient_next_day(recipient)
    else:
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
                    sender.send_recipient_email(recipient, test_next_day=True)
            elif now.minute == 0:
                logging.info("Sleeping.")
            next_minute = datetime(now.year, now.month, now.day, now.hour,
                                   now.minute) + timedelta(minutes=1)
            sleep_time = max(0, ceil(
                (next_minute - datetime.now()).total_seconds()))
            time.sleep(sleep_time)
