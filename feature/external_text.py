from typing import Optional

from feature.text import Text
from utility.system import get_resource_path


class ExternalText(Text):
    def __init__(
            self,
            text_file: str,
            clear_after: bool = False,
            div_style: str = "",
            title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.text_file = text_file
        self.clear_after = clear_after

    def generate_content(self) -> str:
        with open(get_resource_path(self.text_file), "r+") as file:
            self.text = file.read()
            return super().generate_content()

    def on_email_sent(self):
        if self.clear_after:
            open(get_resource_path(self.text_file), "w+").truncate(0)
