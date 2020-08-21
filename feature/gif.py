import logging
import os
from datetime import datetime

from feature.base import Feature
from utility.constant import RESOURCE_PATH
from utility.image import upload_image


class Gif(Feature):

    @property
    def title(self):
        return "云·养花"

    def __init__(self, directory_path: str, start_date_time: datetime,
                 id_multiplier: int = 1, div_style: str = "",
                 image_style: str = ""):
        super().__init__(div_style)
        self.directory_path = directory_path
        self.start_date_time = start_date_time
        self.current_date_time = None  # lazy initialization by Recipient class
        self.id_multiplier = id_multiplier
        self.image_style = image_style

    def generate_html(self) -> str:
        FEATURE_PATH = "gif"
        days = (self.current_date_time - self.start_date_time).days
        gif_id = days * self.id_multiplier
        if gif_id < 10:
            id_string = f"0{gif_id}"
        else:
            id_string = str(gif_id)
        file = list(
                filter(lambda f: f.startswith(f"frame_{id_string}_delay-"),
                       os.listdir(
                               f"{RESOURCE_PATH}/{FEATURE_PATH}/{self.directory_path}"))
        )[0]
        logging.info(f"Gif: {file}")
        image_url = upload_image(
                f"{RESOURCE_PATH}/{FEATURE_PATH}/{self.directory_path}/{file}")
        return f"""<h3><i>第{days + 1}天</i></h3>
<img src='{image_url}' style='{self.image_style}'>
"""
