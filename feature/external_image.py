from typing import Optional

from feature.base import Feature
from utility.file_io import get_resource
from utility.image import upload_image


class ExternalImage(Feature):

    def __init__(self, file_name: Optional[str] = None,
                 image_url: Optional[str] = None,
                 clear_after: bool = False, image_style: str = "",
                 div_style: str = "", title: Optional[str] = None):
        super().__init__(div_style, title)
        self.file_name = file_name
        self.image_url = image_url
        self.image_style = image_style
        self.clear_after = clear_after

    def generate_content(self) -> str:
        image_url = self.image_url if self.file_name is None \
            else upload_image(get_resource(self.file_name))
        self.image_url = image_url  # cache
        return f"<img src='{image_url}' style='{self.image_style}'/>"

    def on_email_sent(self):
        if self.clear_after:
            self.image_style = "display: none;"
