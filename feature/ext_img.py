import os
from typing import Optional

from feature.base import Feature
from utility.constant import CSS_MEDIUM
from utility.system import get_resource_path
from utility.html_builder import html_img
from utility.img import upload_img


class ExternalImage(Feature):
    def __init__(
        self,
        file_name: str = None,
        clear_after: bool = False,
        img_style: str = CSS_MEDIUM,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(div_style, title)
        self.file_path = get_resource_path(file_name)
        self.img_style = img_style
        self.clear_after = clear_after
        self.image_url = None  # lazy
        self.file_path = None

    def generate_content(self) -> str:
        if self.image_url is None:
            if os.path.exists(self.file_path):
                self.image_url = upload_img(self.file_path)  # cache
            else:
                return ""  # empty div, return early
        return html_img(url=self.image_url, style=self.img_style)

    def on_email_sent(self):
        if self.clear_after:
            self.img_style = "display: none; !important"
