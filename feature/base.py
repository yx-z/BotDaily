from abc import ABC, abstractmethod
from typing import Optional

from PIL import ImageFont

from utility.constant import CSS_FULL_WIDTH
from utility.system import get_res_path, FONT_PATH
from utility.html_builder import html_img, html_div
from utility.img import open_img, draw_txt, save_img


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

        background = open_img(get_res_path("feature_background.png"))
        font = ImageFont.truetype(FONT_PATH, text_size)
        title_image = draw_txt(
            background, position, self.title, font, text_color, shadow_color
        )

        header_file = f"feature_header_{self.title}.png"
        save_img(title_image, get_res_path(header_file))
        return html_img(file_name=header_file, style=CSS_FULL_WIDTH)

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

    def get_name(self) -> str:
        return type(self).__name__
