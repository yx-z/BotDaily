from typing import Optional
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
