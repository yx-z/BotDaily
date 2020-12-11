from datetime import datetime
from typing import Optional

from PIL import ImageFont

from feature import ExternalRandomizer
from feature.base import Feature
from utility.constant import DATE_FORMAT
from utility.system import FONT_PATH
from utility.html_builder import html_img
from utility.image import search_unsplash, download_image, draw_text


class Header(Feature):
    def __init__(
        self,
        topic: str,
        text: str,
        start_date: str,
        text_size: int = 42,
        image_style: str = "",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(div_style, title)
        self.text = text
        self.topic = topic
        self.text_size = text_size
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.image_style = image_style
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        image_url = search_unsplash(
            self.topic, (self.current_date_time - self.start_date).days
        )
        image = download_image(image_url)

        width, height = image.size
        left = 0
        top = height / 4
        right = min(1080, width)
        bottom = min(height, top + 400)
        image = image.crop((left, top, right, bottom))

        position = (80, 100)
        text_color = (255, 255, 255)
        border_color = (0, 20, 20)
        font = ImageFont.truetype(FONT_PATH, self.text_size)
        text = (
            f"{self.current_date_time.month}/{self.current_date_time.day} {self.text}"
        )
        image = draw_text(image, position, text, font, text_color, border_color)

        font2 = ImageFont.truetype(FONT_PATH, 32)
        image = draw_text(image, (80, 320), self.topic, font2, text_color, border_color)

        header_file = "header.png"
        image.save(header_file)
        return html_img(file_name="header.png", style=self.image_style)


class RandomHeader(Header):
    def __init__(
        self,
        file_name: str,
        text: str,
        start_date: str,
        end_of_cycle_line: str = "=====\n",
        text_size: int = 42,
        image_style: str = "",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", text, start_date, text_size, image_style, div_style, title)
        self.randomizer = ExternalRandomizer(file_name, end_of_cycle_line)

    def generate_content(self) -> str:
        self.topic = self.randomizer.generate_content()
        return super().generate_content()

    def on_email_sent(self):
        self.randomizer.on_email_sent()
