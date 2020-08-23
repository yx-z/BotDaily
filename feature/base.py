from abc import ABC, abstractmethod
from typing import Optional

from PIL import ImageFont

from utility.constant import RESOURCE_PATH, FONT_NAME, CSS_FULL_WIDTH
from utility.image import open_image, draw_text, save_image, upload_image
from utility.parse import text_to_html


class Feature(ABC):

    def __init__(self, div_style: str = "", title: Optional[str] = None):
        self.div_style = div_style
        self.title = title

    def generate_title(self) -> str:
        if self.title is None:
            return ""

        position = (120, 25)
        text_size = 35
        text_color = (0, 0, 0)
        shadow_color = (255, 255, 255)

        background = open_image(f"{RESOURCE_PATH}/feature_background.png")
        font = ImageFont.truetype(f"{RESOURCE_PATH}/{FONT_NAME}", text_size)
        title_image = draw_text(background, position, self.title, font,
                                text_color, shadow_color)

        out_path = f"{RESOURCE_PATH}/feature_header_{self.title}.png"
        save_image(title_image, out_path)
        return f"<img src='{upload_image(out_path)}' style='{CSS_FULL_WIDTH}'/>"

    def generate_html(self) -> str:
        return text_to_html(
                f"<div style='{self.div_style}'>{self.generate_title()}{self.generate_content()}</div>")

    @abstractmethod
    def generate_content(self) -> str:
        pass
