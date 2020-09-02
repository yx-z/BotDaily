from typing import Optional

from feature.base import Feature
from utility.constant import RESOURCE_PATH


class ExternalText(Feature):
    def __init__(self, text_file: str, div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(div_style, title)
        self.text_file = text_file

    def generate_content(self) -> str:
        return open(f"{RESOURCE_PATH}/{self.text_file}", "r").read()
