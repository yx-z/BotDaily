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
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        logging.basicConfig(level=logging.INFO,
                            format="%(asctime)s %(levelname)-8s %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

        TIME_TO_RECIPIENTS = eval(
            open("configuration/recipient.py", "r").read())
        for _, recipients in TIME_TO_RECIPIENTS.items():
            for recipient in recipients:
                recipient.email_address = SENDER_EMAIL


                def no_op():
                    pass


                recipient.on_email_sent = no_op
                recipient.set_current_date_time(datetime.now())
                sender.send_recipient_email(recipient, timeout_seconds=60,
                                            send_self=True, retry=0,
                                            test_next_day=False)
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
                                                send_self=True, retry=0,
                                                test_next_day=True)
            elif now.minute == 0:
                logging.info("Sleeping.")
            next_minute = datetime(now.year, now.month, now.day, now.hour,
                                   now.minute) + timedelta(minutes=1)
            sleep_time = max(0, ceil(
                (next_minute - datetime.now()).total_seconds()))
            time.sleep(sleep_time)
