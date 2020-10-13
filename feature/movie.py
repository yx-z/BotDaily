import json
from datetime import datetime

from feature.base import Feature
from utility.file_io import get_resource
from utility.html_builder import html_div

MOVIE_PATH = "movie"


class Movie(Feature):

    def __init__(self, order_file_name: str, start_date_time: datetime,
                 div_style: str = "", title: str = "云·电影"):
        super().__init__(div_style, title)
        self.order_file_name = order_file_name
        self.start_date_time = start_date_time
        self.current_date_time = datetime.now()

    def generate_content(self) -> str:
        movie_list = json.load(
                open(get_resource(f"{MOVIE_PATH}/{self.order_file_name}"),
                     "r"))
        days = (self.current_date_time - self.start_date_time).days
        index = movie_list[days]
        html = open(get_resource(f"{MOVIE_PATH}/{index}.html"), "r").read()
        return html_div(inner_html=html, style=self.div_style)
