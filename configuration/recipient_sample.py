from datetime import datetime

from feature.gif import Gif
from feature.greet import Greet
from feature.header import Header
from feature.music import Music
from feature.one import OneCover, OneQuote
from feature.poem import Poem
from feature.weather import Weather
from feature.zhihu_story import ZhihuStory
from mail.recipient import Recipient
from mail.subject import Subject
from utility.constant import CSS_DEFAULT_DIV, CSS_FULL_WIDTH, CSS_CENTER, \
    CSS_SMALL, CSS_MEDIUM

TIME_TO_RECIPIENTS = {
    "08:00": [
        Recipient("123@123.123", Subject("Bot 早报"), [
            Header(["cloud"], "Bot 早报", image_style=CSS_FULL_WIDTH,
                   start_date_time=datetime(2020, 8, 4)),
            Greet("123", start_date_time=datetime(2020, 7, 28)),
            Weather(123, 123, "123", title=None),
            Poem(),
            Gif("bloom1", start_date_time=datetime(2020, 8, 24),
                image_style=CSS_MEDIUM, div_style=CSS_CENTER),
            Music("favorite_music.json", start_date_time=datetime(2020, 8, 17),
                  div_style=CSS_CENTER, image_style=CSS_SMALL),
            OneCover(image_style=CSS_MEDIUM),
            OneQuote(div_style=CSS_CENTER, title=None),
            ZhihuStory("answer_id.txt", start_date_time=datetime(2020, 8, 4))
        ], div_style=CSS_DEFAULT_DIV)
    ]
}
