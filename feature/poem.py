import requests

from feature.base import Feature


class Poem(Feature):

    @property
    def title(self) -> str:
        return "今日诗词"

    def __init__(self, div_style: str = ""):
        super().__init__(div_style)
        self.token = None

    def generate_content(self) -> str:
        if self.token is None:
            self.token = requests.get("https://v2.jinrishici.com/token").json()[
                "data"]

        url = "https://v2.jinrishici.com/sentence"
        data = requests.get(url, headers={"X-User-Token": self.token}).json()[
            "data"]
        poem = data["origin"]
        return f"""{data["content"]}
—— {poem["dynasty"]}·{poem["author"]} 《{poem["title"]}》
"""
