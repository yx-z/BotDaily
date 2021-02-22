from typing import Optional

from utility.constant import CSS_SMALL, CSS_CENTER

import requests

from feature.base import Feature
from utility.html_builder import html_img, html_a, html_div

USER_AGENT = {"User-agent": "Mozilla/5.0"}


class ZhihuDaily(Feature):
    def __init__(self, div_style: str = "", title: Optional[str] = "知乎分享"):
        super().__init__(div_style, title)

    def generate_content(self) -> str:
        stories_url = "https://news-at.zhihu.com/api/4/stories/latest"
        stories = requests.get(stories_url, headers=USER_AGENT).json()["stories"]
        return "".join(
            map(
                lambda story: f"{html_img(url=story['images'][0], style=CSS_SMALL)}{html_div(inner_html=html_a(text=story['title'], url=story['url']), style=CSS_CENTER)}",
                stories,
            )
        )
