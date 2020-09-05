import json
from datetime import datetime
from typing import Optional

from feature.base import Feature
from utility.constant import RESOURCE_PATH

MOVIE_PATH = "movie"


class Movie(Feature):

    def __init__(self, order_file_name: str, start_date_time: datetime,
                 div_style: str = "", title: Optional[str] = "云·电影"):
        super().__init__(div_style, title)
        self.order_file_name = order_file_name
        self.start_date_time = start_date_time
        self.current_date_time = datetime.now()

    def generate_content(self) -> str:
        movie_list = json.load(
                open(f"{RESOURCE_PATH}/{MOVIE_PATH}/{self.order_file_name}",
                     "r"))
        days = (self.current_date_time - self.start_date_time).days
        index = movie_list[days]
        html = open(f"{RESOURCE_PATH}/{MOVIE_PATH}/{index}.html", "r").read()
        return f"<div style='{self.div_style}'>{html}</div>"
