import logging
import os
import time

from configuration.secret import LOG_FILE, SENDER_EMAIL, SENDER_PASSWORD
from mail.sender import GmailSender
from utility.constant import *
from datetime import datetime
from mail.recipient import Recipient
from mail.subject import Subject
from feature import *

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=LOG_FILE)
    logging.info(f"PID - {os.getpid()}")

    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
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
        time.sleep(SECONDS_IN_MINUTE)
