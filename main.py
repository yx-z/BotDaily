import logging
import os
import sys
import time
from datetime import datetime
from importlib import reload

import configuration.recipient as rep
from configuration.secret import LOG_FILE, SENDER_EMAIL, SENDER_PASSWORD
from mail.sender import GmailSender

SECONDS_IN_MINUTE = 60

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
        if now_str in rep.TIME_TO_RECIPIENTS.keys():
            for recipient in rep.TIME_TO_RECIPIENTS[now_str]:
                sender.send_recipient_email(recipient, timeout_seconds=60,
                                            send_self=True, retry=2,
                                            test_next_day=True)
                recipient.set_current_date_time(now)
        elif now.minute == 0:
            logging.info("Sleeping.")
        time.sleep(SECONDS_IN_MINUTE)
        rep = reload(sys.modules["configuration.recipient"])
