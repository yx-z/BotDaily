import json
from datetime import datetime
from typing import Optional, Tuple, List

import requests

from configuration.secret import SENDER_EMAIL, SENDER_PASSWORD
from feature.base import Feature
from utility.constant import DATE_FORMAT, CSS_SMALL, CSS_CENTER
from utility.google_keep import GoogleKeep
from utility.system import get_res_path
from utility.html_builder import html_img, html_from_txt, html_a


class Music(Feature):
    def __init__(
        self,
        content: Optional[str] = None,
        img_style: str = CSS_SMALL,
        div_style: str = CSS_CENTER,
        title: Optional[str] = "云·音乐",
    ):
        super().__init__(div_style, title)
        self.img_style = img_style
        self.content = content

    def generate_content(self) -> str:
        return html_from_txt(self.content)

    def _extract_content(self, netease_tuple: List) -> str:
        music_id, name, author, comment = netease_tuple
        music_data = requests.get(
            f"http://localhost:3000/song/detail?ids={music_id}"
        ).json()["songs"][0]
        album_cover_url = music_data["al"]["picUrl"]

        netease_url = f"https://y.music.163.com/m/song?id={music_id}"
        youtube_url = f"https://youtube.com/results?search_query={name} {author}"
        return f"""{html_img(url=album_cover_url, style=self.img_style)}
曲名: {name}
作者: {author}
{html_a(text="网易云", url=netease_url)}
{html_a(text="YouTube", url=youtube_url)}
    
{comment}
    """

    def _parse_raw_content(self, content: List[str]) -> None:
        """
        :param content: either a [chunk of content] or a netease list as [id, name, author, comment]
        """
        if len(content) == 1:
            self.content = content[0]
        else:
            self.content = self._extract_content(content)


class ExtMusic(Music):
    def __init__(
        self,
        file_name: str,
        start_date: str,
        div_style: str = CSS_CENTER,
        img_style: str = CSS_SMALL,
        title: Optional[str] = "云·音乐",
    ):
        super().__init__(div_style=div_style, img_style=img_style, title=title)
        self.file_path = get_res_path(file_name)
        self.start_date = datetime.strptime(start_date, DATE_FORMAT)
        self.current_date_time = None

    def generate_content(self) -> str:
        music_list = json.load(open(self.file_path, "r"))
        days = (self.current_date_time - self.start_date).days
        content = music_list[len(music_list) - days - 2]
        self._parse_raw_content(content)
        return super().generate_content()


class GoogleKeepMusic(Music):
    def __init__(
        self,
        google_keep_name: str,
        clear_after: bool = False,
        div_style: str = CSS_CENTER,
        img_sytle: str = CSS_SMALL,
        title: Optional[str] = "云·音乐",
    ):
        super().__init__(div_style=div_style, img_style=img_sytle, title=title)
        self.clear_after = clear_after
        self.keep = GoogleKeep(SENDER_EMAIL, SENDER_PASSWORD, google_keep_name)

    def generate_content(self) -> str:
        content = self.keep.get_note_txt().split("\n")
        self._parse_raw_content(content)
        return super().generate_content()

    def on_email_sent(self):
        if self.clear_after:
            self.keep.clear_note()
