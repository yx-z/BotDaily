from typing import Optional

from feature.base import Feature
from utility.html_builder import html_from_text


class Text(Feature):

    def __init__(self, text: str, div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(div_style, title)
        self.text = text

    def generate_content(self) -> str:
        return html_from_text(self.text)
