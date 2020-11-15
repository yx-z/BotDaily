from abc import ABC, abstractmethod
from typing import Optional

from PIL import ImageFont

from utility.constant import CSS_FULL_WIDTH
from utility.system import get_resource_path, FONT_PATH
from utility.html_builder import html_img, html_div
from utility.image import open_image, draw_text, save_image


class Feature(ABC):
    def __init__(self, div_style: str = "", title: Optional[str] = None):
        self.div_style = div_style
        self.title = title

    def generate_title(self) -> str:
        if self.title is None or len(self.title.strip()) == 0:
            return ""

        position = (120, 25)
        text_size = 30
        text_color = (0, 0, 0)
        shadow_color = (255, 255, 255)

        background = open_image(get_resource_path("feature_background.png"))
        font = ImageFont.truetype(FONT_PATH, text_size)
        title_image = draw_text(
            background, position, self.title, font, text_color, shadow_color
        )

        out_path = get_resource_path(f"feature_header_{self.title}.png")
        save_image(title_image, out_path)
        return html_img(path=out_path, style=CSS_FULL_WIDTH)

    @abstractmethod
    def generate_content(self) -> str:
        pass

    def generate_html(self) -> str:
        return html_div(
            inner_html=f"{self.generate_title()}{self.generate_content()}",
            style=self.div_style,
        )

    def on_email_sent(self):
        pass
