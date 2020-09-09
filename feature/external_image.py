from typing import Optional

from feature.base import Feature
from utility.constant import RESOURCE_PATH
from utility.image import upload_image


class ExternalImage(Feature):

    def __init__(self, file_name: Optional[str] = None,
                 image_url: Optional[str] = None, image_style: str = "",
                 div_style: str = "", title: Optional[str] = None):
        super().__init__(div_style, title)
        self.file_name = file_name
        self.image_url = image_url
        self.image_style = image_style

    def generate_content(self) -> str:
        image_url = self.image_url if self.file_name is None \
            else upload_image(f"{RESOURCE_PATH}/{self.file_name}")
        return f"<img src='{image_url}' style='{self.image_style}'/>"
