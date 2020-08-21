import logging
import os
from datetime import datetime

from configuration.secret import TEST_SENDER_PASSWORD
from feature.gif import Gif
from feature.music import Music
from feature.subject import Subject
from mail.recipient import Recipient
from mail.sender import GmailSender

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    current_date_time = datetime.now()

    os.system("node netease-api/app.js &")
    test_recipient = Recipient("wilsonzyx@gmail.com", current_date_time,
                               Subject("Hi"),
                               [Music("favorite_music.json", current_date_time),
                                Gif("bloom", current_date_time)],
                               "font-size: 1.15em; color: #000; padding: 5px;")

    test_sender = GmailSender("wilsonzyx@gmail.com", TEST_SENDER_PASSWORD)
    test_sender.send_recipient_email(test_recipient, test_next_day=False)
