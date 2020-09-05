from typing import Optional

from feature.base import Feature
from utility.constant import RESOURCE_PATH


class ExternalText(Feature):
    def __init__(self, text_file: str, clear_after: bool = False,
                 div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(div_style, title)
        self.text_file = text_file
        self.clear_after = clear_after

    def generate_content(self) -> str:
        with open(f"{RESOURCE_PATH}/{self.text_file}", "r+") as file:
            text = file.read()
            file.truncate(0)
            return text
