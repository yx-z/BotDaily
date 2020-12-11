import json
from datetime import datetime
from typing import Optional

from feature.base import Feature
from utility.constant import DATE_FORMAT
from utility.system import get_resource_path
from utility.html_builder import html_div

MOVIE_PATH = "movie"


class Movie(Feature):
    def __init__(
        self,
        order_file_name: str,
        start_date: str,
        div_style: str = "",
        title: Optional[str] = "云·电影",
    ):
        super().__init__(div_style, title)
        self.order_file_name = order_file_name
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.current_date_time = None

    def generate_content(self) -> str:
        movie_list = json.load(
            open(get_resource_path(f"{MOVIE_PATH}/{self.order_file_name}"), "r")
        )
        days = (self.current_date_time - self.start_date).days
        index = movie_list[days]
        html = open(get_resource_path(f"{MOVIE_PATH}/{index}.html"), "r").read()
        return html_div(inner_html=html, style=self.div_style)
