from datetime import datetime
from typing import Optional

from feature.base import Feature
from utility.constant import CSS_FULL_WIDTH, DATE_FORMAT
from utility.html_builder import html_img


class AbsoluteKid(Feature):
    def __init__(
        self,
        start_date: str,
        div_style: str = "",
        img_style: str = CSS_FULL_WIDTH,
        title: Optional[str] = "绝对小孩",
    ):
        super().__init__(div_style, title)
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.img_style = img_style
        self.current_date_time = None

    def generate_content(self) -> str:
        days = (self.current_date_time - self.start_date).days
        indices = [days * 2 - 1, days * 2]
        urls = list(
            map(
                lambda i: f"https://raw.githubusercontent.com/yx-z/YunDaily/master/Yun/res/absolute-kids/{f'00{i}'[-3:]}.jpg",
                indices,
            )
        )
        return f"""
{html_img(url=urls[0], style=self.img_style)}
{html_img(url=urls[1], style=self.img_style)}
"""
