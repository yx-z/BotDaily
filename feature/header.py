import random
from datetime import datetime
from typing import List, Optional

from PIL import ImageFont

from feature.base import Feature
from utility.constant import DATE_FORMAT
from utility.system import get_resource_path, FONT_PATH
from utility.html_builder import html_img
from utility.image import search_unsplash, download_image, draw_text


class Header(Feature):
    def __init__(
        self,
        topic: List[str],
        text: str,
        start_date: str,
        text_size: int = 42,
        image_style: str = "",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(div_style, title)
        self.text = text
        self.topics = topic
        self.text_size = text_size
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.image_style = image_style
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        topic = random.choice(self.topics)
        image_url = search_unsplash(
            topic, (self.current_date_time - self.start_date).days
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
        image = draw_text(image, (80, 320), topic, font2, text_color, border_color)

        header_file = "header.png"
        image.save(header_file)
        return html_img(file_name="header.png", style=self.image_style)
