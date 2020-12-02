import random
from typing import Optional, List
from feature.base import Feature


class End(Feature):
    def __init__(
        self, sender_name: str, days: List[str], div_style: str = "", title: Optional[str] = None
    ):
        super().__init__( div_style, title, )
        self.sender_name = sender_name
        self.days = days

    def generate_content(self) -> str:
        return f"""
-----
祝{random.choice(self.days)}的一天。

你的 {self.sender_name}
"""
