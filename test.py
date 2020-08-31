import logging
import os
from datetime import datetime

from configuration.secret import SENDER_PASSWORD, SENDER_EMAIL
from feature.AbsoluteKid import AbsoluteKid
from feature.end import End
from feature.gif import Gif
from feature.greet import Greet
from feature.header import Header
from feature.music import Music
from feature.one import OneCover, OneQuote
from feature.poem import Poem
from feature.text import Text
from feature.weather import Weather
from feature.zhihu_daily import ZhihuDaily
from feature.zhihu_story import ZhihuStory
from mail.recipient import Recipient
from mail.sender import GmailSender
from mail.subject import Subject
from utility.constant import CSS_CENTER, CSS_MEDIUM, CSS_SMALL, CSS_FULL_WIDTH

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)-8s %(message)s",
                        datefmt="%Y-%m-%d %H:%M:%S")

    current_date_time = datetime.now()

    os.system("node netease-api/app.js &")
    test_recipient = Recipient("wilsonzyx@gmail.com", Subject("Bot Daily"),
                               [Header("cloud", "Bot Daily",
                                       start_date_time=current_date_time,
                                       image_style=CSS_FULL_WIDTH),
                                Greet("hi", start_date_time=current_date_time),
                                ZhihuDaily(div_style="font-size: 1em;"),
                                ZhihuStory("answer_id.txt",
                                           start_date_time=current_date_time),
                                Weather(1, 1, "test_city_name", title=None),
                                Poem(),
                                AbsoluteKid(
                                    start_date_time=datetime(2020, 8, 29)),
                                OneCover(image_style=CSS_MEDIUM),
                                OneQuote(div_style=CSS_CENTER, title=None),
                                Music("favorite_music.json",
                                      start_date_time=current_date_time,
                                      div_style=CSS_CENTER,
                                      image_style=CSS_SMALL),
                                Text("custom text", "TITLE"),
                                Gif("bloom",
                                    start_date_time=current_date_time,
                                    div_style=CSS_CENTER,
                                    image_style=CSS_MEDIUM),
                                End("Bot")])
    test_recipient.add_current_date_time(current_date_time)

    test_sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    test_sender.send_recipient_email(test_recipient, timeout_seconds=60)
