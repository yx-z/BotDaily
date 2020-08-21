import logging
import os
from datetime import datetime

from configuration.secret import TEST_SENDER_PASSWORD
from feature.end import End
from feature.gif import Gif
from feature.greet import Greet
from feature.header import Header
from feature.music import Music
from feature.text import Text
from feature.weather import Weather
from mail.recipient import Recipient
from mail.sender import GmailSender
from mail.subject import Subject
from utility.constant import CSS_CENTER, CSS_MEDIUM

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    current_date_time = datetime.now()

    os.system("node netease-api/app.js &")
    test_recipient = Recipient("yx.z@hotmail.com", current_date_time,
                               Subject("Bot Daily"),
                               [Greet("David",
                                      know_date_time=current_date_time),
                                Header("cloud", "Bot Daily",
                                       start_date_time=current_date_time),
                                Weather(1, 1, "city_name"),
                                Music("favorite_music.json",
                                      start_date_time=current_date_time,
                                      div_style=CSS_CENTER,
                                      image_style=CSS_MEDIUM),
                                Text("custom text"),
                                Gif("bloom",
                                    start_date_time=current_date_time,
                                    div_style=CSS_CENTER,
                                    image_style=CSS_MEDIUM),
                                End("Bot")])

    test_sender = GmailSender("wilsonzyx@gmail.com", TEST_SENDER_PASSWORD)
    test_sender.send_recipient_email(test_recipient, retry=1,
                                     timeout_seconds=20,
                                     test_next_day=True)
