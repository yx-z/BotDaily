import logging
import os
from datetime import datetime

from configuration.secret import SENDER_PASSWORD, SENDER_EMAIL
from feature.absolute_kid import AbsoluteKid
from feature.end import End
from feature.gif import Gif
from feature.greet import Greet
from feature.header import Header
from feature.music import Music
from feature.one import OneCover, OneQuote
from feature.movie import Movie
from feature.poem import Poem
from feature.text import Text
from feature.external_text import ExternalText
from feature.external_image import ExternalImage
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
    test_recipient = Recipient("wilsonzyx@gmail.com", Subject("Bot Daily"), [Music("favorite_music.json", start_date_time=datetime(2020,9,24), div_style=CSS_CENTER, image_style=CSS_MEDIUM), ZhihuStory("answer_id.txt", start_date_time=datetime(2020, 8, 4))])
    test_recipient.set_current_date_time(current_date_time)

    test_sender = GmailSender(SENDER_EMAIL, SENDER_PASSWORD)
    test_sender.send_recipient_email(test_recipient, timeout_seconds=60, send_self=True)
