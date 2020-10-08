from typing import Optional

from feature.text import Text
from utility.parse import PARSE_NEW_LINE


class End(Text):

    def __init__(self, sender_name: str = "Bot", div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(f"""
-----
你的,
{sender_name}
""", div_style, title, PARSE_NEW_LINE)
