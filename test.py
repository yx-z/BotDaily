import logging
from datetime import datetime

from configuration.secret import TEST_SENDER_PASSWORD
from feature.end import End
from feature.gif import Gif
from feature.greet import Greet
from feature.header import Header
from feature.subject import Subject
from feature.weather import Weather
from mail.recipient import Recipient
from mail.sender import GmailSender
from utility.constant import CSS_SMALL

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    current_date_time = datetime.now()

    test_recipient = Recipient("wilsonzyx@gmail.com", current_date_time,
                               Subject("Hi"),
                               [Header("cloud", "Bot Daily",
                                       datetime(2020, 1, 1)),
                                Greet("David", datetime(2020, 1, 20)),
                                Gif("bloom", datetime(2020, 8, 21),
                                    image_style=CSS_SMALL),
                                Weather(1, 1, "hi"), End()],
                               "font-size: 1.15em; color: #000; padding: 5px;")

    test_sender = GmailSender("wilsonzyx@gmail.com", TEST_SENDER_PASSWORD)
    test_sender.send_recipient_email(test_recipient)
