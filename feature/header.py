import random
from datetime import datetime
from typing import Optional, List

from PIL import ImageFont

from feature.base import Feature
from utility.constant import FONT_NAME, RESOURCE_PATH
from utility.image import search_unsplash, download_image, upload_image, \
    draw_text


class Header(Feature):

    def __init__(self, topic: List[str], text: str, start_date_time: datetime,
                 text_size: int = 40, image_style: str = "",
                 div_style: str = "", title: Optional[str] = None):
        super().__init__(div_style, title)
        self.text = text
        self.topics = topic
        self.text_size = text_size
        self.start_date_time = start_date_time
        self.image_style = image_style
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        topic = random.choice(self.topics)
        image_url = search_unsplash(topic, (
                self.current_date_time - self.start_date_time).days)
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
        font = ImageFont.truetype(f"{RESOURCE_PATH}/{FONT_NAME}",
                                  self.text_size)
        text = f"{self.current_date_time.month}/{self.current_date_time.day} {self.text}"
        image = draw_text(image, position, text, font, text_color, border_color)

        font2 = ImageFont.truetype(f"{RESOURCE_PATH}/{FONT_NAME}", 28)
        image = draw_text(image, (80, 360), topic, font2, text_color,
                          border_color)

        out_path = f"{RESOURCE_PATH}/header.png"
        image.save(out_path)
        return f"<img src='{upload_image(out_path)}' style='{self.image_style}'/>"
