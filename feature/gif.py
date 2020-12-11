import logging
import os
from datetime import datetime
from typing import Optional

from feature.base import Feature
from utility.system import get_resource_path
from utility.html_builder import html_tag, html_img, html_emphasis


class Gif(Feature):
    def __init__(
        self,
        directory_path: str,
        start_date_time: datetime,
        id_multiplier: int = 1,
        div_style: str = "",
        image_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(div_style, title)
        self.directory_path = directory_path
        self.start_date_time = start_date_time
        self.current_date_time = None  # lazy initialization by Recipient class
        self.id_multiplier = id_multiplier
        self.image_style = image_style

    def generate_content(self) -> str:
        FEATURE_PATH = "gif"
        days = (self.current_date_time - self.start_date_time).days
        gif_id = days * self.id_multiplier
        if gif_id < 10:
            id_string = f"0{gif_id}"
        else:
            id_string = str(gif_id)
        file = list(
            filter(
                lambda f: f.startswith(f"frame_{id_string}_delay-"),
                os.listdir(get_resource_path(f"{FEATURE_PATH}/{self.directory_path}")),
            )
        )[0]
        logging.info(f"Gif: {file}")
        return f"""{html_tag("h3", paired=True, inner_html=html_emphasis(f"第{days + 1}天"))}
{html_img(file_name=f"{FEATURE_PATH}/{self.directory_path}/{file}", style=self.image_style)}
"""
