import logging
import os
import time
from datetime import datetime

from configuration.recipient import TIME_TO_RECIPIENTS
from configuration.secret import LOG_FILE, SENDER_EMAIL, SENDER_PASSWORD
from mail.sender import GmailSender

SECONDS_IN_MINUTE = 60

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S",
                        filename=LOG_FILE)
    logging.info("PID - {}.".format(os.getpid()))

    sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    while True:
        now = datetime.now()
        now_str = now.strftime("%H:%M")
        if now_str in TIME_TO_RECIPIENTS.keys():
            for recipient in TIME_TO_RECIPIENTS[now_str]:
                recipient.set_current_date_time(now)
                sender.send_recipient_email(recipient, timeout_seconds=60,
                                            send_self=True, retry=2,
                                            test_next_day=True)
        elif now.minute == 0:
            logging.info("Sleeping.")
        time.sleep(SECONDS_IN_MINUTE)
