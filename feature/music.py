import json
from datetime import datetime
from typing import Optional

import requests

from feature.base import Feature
from utility.file_io import get_resource
from utility.html_builder import build_html_img, build_html_tag, \
    build_html_from_text


class Music(Feature):

    def __init__(self, file_name: str, start_date_time: datetime,
                 div_style: str = "", image_style: str = "",
                 title: Optional[str] = "云·音乐"):
        super().__init__(div_style, title)
        self.file_name = file_name
        self.start_date_time = start_date_time
        self.current_date_time = None
        self.image_style = image_style

    def generate_content(self) -> str:
        music_list = json.load(open(get_resource(self.file_name), "r"))
        days = (self.current_date_time - self.start_date_time).days
        music_today = music_list[len(music_list) - days - 2]

        has_id_only = len(music_today) == 2  # [music_id, comment]
        if has_id_only:
            music_id = music_today[0]
        else:  # [music_name, music_author, comment]
            music_name = music_today[0]
            music_author = music_today[1]
            search_data = requests.get(
                    f"http://localhost:3000/search?keywords={music_name}, {music_author}").json()
            music_id = search_data["result"]["songs"][0]["id"]

        music_data = requests.get(
                f"http://localhost:3000/song/detail?ids={music_id}").json()[
            "songs"][0]
        if has_id_only:
            music_name = music_data["name"]
            music_author = music_data["ar"][0]["name"]
        album_cover_url = music_data["al"]["picUrl"]

        netease_url = f"https://y.music.163.com/m/song?id={music_id}"
        youtube_url = f"https://youtube.com/results?search_query={music_name}, {music_author}"
        return build_html_from_text(
                f"""{build_html_img(image_url=album_cover_url, image_style=self.image_style)}
    曲名: {music_name}
    作者: {music_author}
    {build_html_tag("a", href={netease_url}, inner_html="网易云")}
    {build_html_tag("a", href={youtube_url}, inner_html="YouTube")}
    
    {music_today[-1]}
    """,
                parse_angle_brackets=False)  # don't parse angle brackets for having image tags
