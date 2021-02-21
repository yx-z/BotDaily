from typing import List, Dict, Optional
from utility.constant import CSS_SMALL, CSS_CENTER

import requests
from bs4 import BeautifulSoup

from feature.base import Feature

USER_AGENT = {"User-agent": "Mozilla/5.0"}


class ZhihuDaily(Feature):
    def __init__(self, div_style: str = "", title: Optional[str] = "知乎日报"):
        super().__init__(div_style, title)

    def generate_content(self) -> str:
        stories_url = "https://news-at.zhihu.com/api/4/stories/latest"
        stories = requests.get(stories_url, headers=USER_AGENT).json()["stories"]
        html = ""
        for story in stories:
            html += f"""
<div style="padding: 5px;">
<img src="{story['images'][0]}" style="{CSS_SMALL}">
<div style="{CSS_CENTER}"><a href="{story['url']}">{story['title']}</a></div>
</div>
"""
        return html
