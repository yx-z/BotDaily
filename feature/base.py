from abc import ABC, abstractmethod

from PIL import ImageFont

from utility.constant import RESOURCE_PATH, FONT_NAME, CSS_FULL_WIDTH
from utility.image import open_image, draw_text, save_image, upload_image


class Feature(ABC):

    @property
    def title(self) -> str:
        return ""

    @property
    def background_path(self) -> str:
        return f"{RESOURCE_PATH}/feature_background.png"

    def generate_title_html(self) -> str:
        if self.title == "":
            return ""

        position = (120, 25)
        text_size = 35
        text_color = (0, 0, 0)
        shadow_color = (255, 255, 255)

        background = open_image(self.background_path)
        font = ImageFont.truetype(f"{RESOURCE_PATH}/{FONT_NAME}", text_size)
        title_image = draw_text(background, position, self.title, font,
                                text_color, shadow_color)

        out_path = f"{RESOURCE_PATH}/feature_header_{self.title}.png"
        save_image(title_image, out_path)
        return f"<img src='{upload_image(out_path)}' style='{CSS_FULL_WIDTH}'/>"

    @abstractmethod
    def generate_html(self) -> str:
        pass
