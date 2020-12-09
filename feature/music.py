import json
from datetime import datetime
from typing import Optional

import requests

from feature.base import Feature
from utility.system import get_resource_path
from utility.html_builder import html_img, html_from_text, html_a


class Music(Feature):
    def __init__(
        self,
        file_name: str,
        start_date_time: datetime,
        div_style: str = "",
        image_style: str = "",
        title: Optional[str] = "云·音乐",
    ):
        super().__init__(div_style, title)
        self.file_path = get_resource_path(file_name)
        self.start_date_time = start_date_time
        self.current_date_time = None
        self.image_style = image_style

    def generate_content(self) -> str:
        music_list = json.load(open(self.file_path, "r"))
        days = (self.current_date_time - self.start_date_time).days
        content = music_list[len(music_list) - days - 2]
        if len(content) == 1:
            return html_from_text(content[0], parse_angle_brackets=False)

        music_id, name, author, comment = content
        music_data = requests.get(
            f"http://localhost:3000/song/detail?ids={music_id}"
        ).json()["songs"][0]
        album_cover_url = music_data["al"]["picUrl"]

        netease_url = f"https://y.music.163.com/m/song?id={music_id}"
        youtube_url = f"https://youtube.com/results?search_query={name}, {author}"
        return html_from_text(
            f"""{html_img(url=album_cover_url, style=self.image_style)}
    曲名: {name}
    作者: {author}
    {html_a(text="网易云", url=netease_url)}
    {html_a(text="YouTube", url=youtube_url)}
    
    {comment}
    """,
            parse_angle_brackets=False,
        )
