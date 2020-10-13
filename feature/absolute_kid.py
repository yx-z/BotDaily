from datetime import datetime

from feature.base import Feature
from utility.constant import CSS_FULL_WIDTH
from utility.html_builder import html_img


class AbsoluteKid(Feature):

    def __init__(self, start_date_time: datetime, div_style: str = "",
                 image_style: str = CSS_FULL_WIDTH, title: str = "绝对小孩"):
        super().__init__(div_style, title)
        self.start_date_time = start_date_time
        self.image_style = image_style
        self.current_date_time = None

    def generate_content(self) -> str:
        days = (self.current_date_time - self.start_date_time).days
        indices = [days * 2 - 1, days * 2]
        urls = list(map(lambda
                            i: f"https://raw.githubusercontent.com/yx-z/YunDaily/master/Yun/res/absolute-kids/{f'00{i}'[-3:]}.jpg",
                        indices))
        return f"""
{html_img(image_url=urls[0], image_style=self.image_style)}
{html_img(image_url=urls[1], image_style=self.image_style)}
"""
