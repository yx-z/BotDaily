from datetime import datetime
from typing import Optional

from PIL import ImageFont

from feature import ExtRand
from feature.base import Feature
from utility.constant import DATE_FORMAT, CSS_FULL_WIDTH
from utility.system import FONT_PATH, get_res_path
from utility.html_builder import html_img
from utility.img import search_unsplash, dl_img, draw_txt

HEADER_FILE = "header.png"


class Header(Feature):
    def __init__(
        self,
        topic: str,
        txt: str,
        start_date: str,
        txt_size: int = 42,
        img_style: str = CSS_FULL_WIDTH,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(div_style, title)
        self.txt = txt
        self.topic = topic
        self.txt_size = txt_size
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.img_style = img_style
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        img_url = search_unsplash(
            self.topic, (self.current_date_time - self.start_date).days
        )
        img = dl_img(img_url)

        width, height = img.size
        left = 0
        top = height / 4
        right = min(1080, width)
        bottom = min(height, top + 400)
        img = img.crop((left, top, right, bottom))

        position = (80, 100)
        text_color = (255, 255, 255)
        border_color = (0, 20, 20)
        font = ImageFont.truetype(FONT_PATH, self.txt_size)
        txt = (
            f"{self.current_date_time.month}/{self.current_date_time.day} {self.txt}"
        )
        img = draw_txt(img, position, txt, font, text_color, border_color)

        font2 = ImageFont.truetype(FONT_PATH, 32)
        img = draw_txt(img, (80, 320), self.topic, font2, text_color, border_color)

        img.save(get_res_path(HEADER_FILE))
        return html_img(file_name=HEADER_FILE, style=self.img_style)


class RandHeader(Header):
    def __init__(
        self,
        file_name: str,
        txt: str,
        start_date: str,
        end_of_cycle_line: str = "=====",
        txt_size: int = 42,
        img_style: str = "",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", txt, start_date, txt_size, img_style, div_style, title)
        self.randomizer = ExtRand(file_name, end_of_cycle_line)

    def generate_content(self) -> str:
        self.topic = self.randomizer.generate_content()
        return super().generate_content()

    def on_email_sent(self):
        self.randomizer.on_email_sent()
