from typing import Optional

from feature import ExternalRandomizer
from feature.text import Text


class End(Text):
    def __init__(
        self, sender_name: str, div_style: str = "", title: Optional[str] = None
    ):
        super().__init__(
            "",
            div_style,
            title,
        )
        self.sender_name = sender_name

    def generate_content(self) -> str:
        self.text = f"""
-----
祝美好的一天。

你的 {self.sender_name}
"""
        return super().generate_content()


class RandomEnd(End):
    def __init__(
        self,
        file_name: str,
        sender_name: str,
        end_of_cycle_line: str = "=====",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(sender_name, div_style, title)
        self.randomizer = ExternalRandomizer(file_name, end_of_cycle_line, div_style)

    def generate_content(self) -> str:
        return f"""
=====
祝{self.randomizer.generate_content()}的一天.

你的 {self.sender_name}
"""

    def on_email_sent(self):
        self.randomizer.on_email_sent()
