import logging
import os
import sys
import time

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
    if sys.argv[1] == "test":
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

        TIME_TO_RECIPIENTS = eval(
            open("configuration/recipient.py", "r").read())
        for _, recipients in TIME_TO_RECIPIENTS.items():
            for recipient in recipients:
                recipient.set_current_date_time(datetime.now())
                sender.send_recipient_email(recipient, timeout_seconds=60,
                                            send_self=True, retry=0)
    else:
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S",
                            filename=LOG_FILE)
        logging.info(f"PID - {os.getpid()}")

        while True:
            now = datetime.now()
            now_str = now.strftime("%H:%M")
            TIME_TO_RECIPIENTS = eval(
                open("configuration/recipient.py", "r").read())
            if now_str in TIME_TO_RECIPIENTS.keys():
                for recipient in TIME_TO_RECIPIENTS[now_str]:
                    recipient.set_current_date_time(now)
                    sender.send_recipient_email(recipient, timeout_seconds=60,
                                                send_self=True, retry=0)
            elif now.minute == 0:
                logging.info("Sleeping.")
            next_minute = datetime(now.year, now.month, now.day, now.hour,
                                   now.minute) + timedelta(minutes=1)
            time.sleep(
                max(0, int((next_minute - datetime.now()).total_seconds())))
