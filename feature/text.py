from typing import Optional

from feature.base import Feature
from utility.parse import text_to_html


class Text(Feature):

    def __init__(self, text: str, div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(div_style, title)
        self.text = text

    def generate_content(self) -> str:
        return text_to_html(self.text)
