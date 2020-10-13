from typing import Optional

import requests
from bs4 import BeautifulSoup

from feature.base import Feature

USER_AGENT = {"User-agent": "Mozilla/5.0"}


class ZhihuDaily(Feature):

    def __init__(self, div_style: str = "", title: str = "知乎日报"):
        super().__init__(div_style, title)

    @staticmethod
    def __request_id__() -> Optional[int]:
        stories_url = "https://news-at.zhihu.com/api/3/stories/latest"
        stories = \
            requests.get(stories_url, headers=USER_AGENT).json()[
                "stories"]
        for story in stories:
            if "瞎扯" in story["title"]:
                return story["id"]
        return None

    @staticmethod
    def __request_joke__(joke_id: int) -> str:
        story_url = f"https://news-at.zhihu.com/api/4/news/{joke_id}"
        res = requests.get(story_url, headers=USER_AGENT).json()
        body = res["body"]
        soup = BeautifulSoup(body, "html.parser")
        joke_str = str(soup.find("div", class_="content-inner"))
        filter_idx = joke_str.find("<p>以上瞎扯节选自")
        if filter_idx > 0:
            joke_str = joke_str[:filter_idx]
        return joke_str

    def generate_content(self) -> str:
        joke_id = self.__request_id__()
        if joke_id is None:
            return ""
        else:
            return self.__request_joke__(joke_id)
