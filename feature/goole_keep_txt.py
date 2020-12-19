from typing import Optional

import gkeepapi

from configuration.secret import SENDER_PASSWORD, SENDER_EMAIL
from feature import Txt
from utility.constant import CSS_MEDIUM
from utility.html_builder import html_from_txt, html_img


class GoogleKeepTxt(Txt):
    def __init__(
        self,
        note_id: str,
        clear_after: bool = False,
        img_style: str = CSS_MEDIUM,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.note_id = note_id
        self.clear_after = clear_after
        self.img_style = img_style
        self.keep = gkeepapi.Keep()

    def generate_content(self) -> str:
        self.keep.login(SENDER_EMAIL, SENDER_PASSWORD)
        note = self.keep.get(self.note_id)
        images = map(
            lambda i: html_img(self.keep.getMediaLink(i), style=self.img_style),
            note.images,
        )
        return html_from_txt(f"{note.text}\n{''.join(images)}", parse_list=["\n"])

    def on_email_sent(self):
        if self.clear_after:
            self.keep.login(SENDER_EMAIL, SENDER_PASSWORD)
            note = self.keep.get(self.note_id)
            note.text = ""
