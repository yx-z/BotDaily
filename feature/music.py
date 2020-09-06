import json
from datetime import datetime
from typing import Optional

import requests

from feature.base import Feature
from utility.constant import RESOURCE_PATH
from utility.parse import text_to_html


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
        music_list = json.load(open(f"{RESOURCE_PATH}/{self.file_name}", "r"))
        days = (self.current_date_time - self.start_date_time).days
        music_today = music_list[len(music_list) - days - 2]
        music_name = music_today[0]
        music_author = music_today[1]
        youtube_url = f"https://youtube.com/results?search_query={music_name}, {music_author}"
        data = requests.get(
                f"http://localhost:3000/search?keywords={music_name}, {music_author}").json()
        song_id = data["result"]["songs"][0]["id"]
        netease_url = f"https://y.music.163.com/m/song?id={song_id}"

        album_cover_data = requests.get(
                f"http://localhost:3000/song/detail?ids={song_id}").json()
        album_cover_url = album_cover_data["songs"][0]["al"]["picUrl"]
        return text_to_html(
                f"""<img src="{album_cover_url}" style="{self.image_style}"/>
    曲名: {music_name}
    作者: {music_author}
    <a href="{netease_url}">网易云链接</a>
    <a href="{youtube_url}">搜索Youtube (备用)</a>
    
    {music_today[2]}
    """)
