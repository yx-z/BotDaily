from typing import Optional

from feature.base import Feature
from utility.html_builder import html_img
from utility.image import upload_image


class ExternalImage(Feature):

    def __init__(self, file_name: str = None,
                 clear_after: bool = False, image_style: str = "",
                 div_style: str = "", title: Optional[str] = None):
        super().__init__(div_style, title)
        self.image_url = ""  # lazy
        self.file_name = file_name
        self.image_style = image_style
        self.clear_after = clear_after

    def generate_content(self) -> str:
        if self.image_url == "":
            self.image_url = upload_image(self.file_name)  # cache
        return html_img(self.image_url, image_style=self.image_style)

    def on_email_sent(self):
        if self.clear_after:
            self.image_style = "display: none;"
