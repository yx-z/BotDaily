import os

from feature.base import Feature
from utility.constant import CSS_MEDIUM
from utility.file_io import get_resource
from utility.html_builder import html_img
from utility.image import upload_image


class ExternalImage(Feature):

    def __init__(self, file_name: str = None,
                 clear_after: bool = False, image_style: str = CSS_MEDIUM,
                 div_style: str = "", title: str = None):
        super().__init__(div_style, title)
        self.file_name = file_name
        self.image_style = image_style
        self.clear_after = clear_after
        self.image_url = None  # lazy
        self.file_path = None

    def generate_content(self) -> str:
        if self.image_url is None:
            self.file_path = get_resource(self.file_name)
            self.image_url = upload_image(self.file_path)  # cache
        return html_img(url=self.image_url, style=self.image_style)

    def on_email_sent(self):
        if self.clear_after and self.file_path is not None:
            os.system(f"rm -f {self.file_path}")
