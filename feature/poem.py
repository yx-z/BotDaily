from typing import Optional

import requests

from feature.base import Feature


class Poem(Feature):
    def __init__(self, div_style: str = "", title: Optional[str] = "今日诗词"):
        super().__init__(div_style, title)
        self.token = None

    def generate_content(self) -> str:
        if self.token is None:
            self.token = requests.get("https://v2.jinrishici.com/token").json()["data"]

        url = "https://v2.jinrishici.com/sentence"
        data = requests.get(url, headers={"X-User-Token": self.token}).json()["data"]
        poem = data["origin"]
        return f"""{data["chunk"]}
—— {poem["dynasty"]}·{poem["author"]} 《{poem["title"]}》
"""
