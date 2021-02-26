from typing import Optional

from configuration.secret import SENDER_EMAIL, SENDER_PASSWORD
from feature.base import Feature
from utility.constant import CSS_MEDIUM
from utility.google_keep import GoogleKeep
from utility.html_builder import html_from_txt, html_img
from utility.system import get_res_path


class Txt(Feature):
    def __init__(self, txt: str, div_style: str = "", title: Optional[str] = None):
        super().__init__(div_style, title)
        self.txt = txt

    def generate_content(self) -> str:
        return html_from_txt(self.txt)


class ExternalTxt(Txt):
    def __init__(
        self,
        file_name: str,
        as_python: bool = False,
        clear_after: bool = False,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.file_path = get_res_path(file_name)
        self.clear_after = clear_after
        self.as_python = as_python

    def generate_content(self) -> str:
        with open(self.file_path, "r") as file:
            self.txt = file.read()
            if self.as_python:
                self.txt = html_from_txt(eval(self.txt), exclude_parse_list=["<", ">"])
            return super().generate_content()

    def on_email_sent(self):
        if self.clear_after:
            with open(self.file_path, "w+") as file:
                file.truncate(0)
                if self.as_python:
                    file.write(
                        '''# html_tag(name: str, paired: bool = False, inner_html: str = "", **kwargs)
# html_img(url: Optional[str] = None, path: str = "", style: str = "", **kwargs)
# html_div(inner_html: str, style: str = "", **kwargs)
# html_emphasis(txt: str, bold: bool = True, italic: bool = True)
# html_a(txt: str, url: str, style: str = "", **kwargs)

# HTML_NEW_LINE = "<br>"
# HTML_LESS_THAN_TEXT = "&lt;"
# HTML_GREATER_THAN_TEXT = "&gt;"

# CSS_DEFAULT_DIV = "font-size: 1.15em; color: #000; padding: 5px;"
# CSS_FULL_WIDTH = "width: 100%;"
# CSS_CENTER = "txt-align: center;"
# CSS_BIG = "display: block; width: 90%; margin: auto;"
# CSS_MEDIUM = "display: block; width: 60%; margin: auto;"
# CSS_SMALL = "display: block; width: 40%; margin: auto;"

# get_resource_path(path: str)

f"""


"""

'''
                    )


class GoogleKeepTxt(Txt):
    def __init__(
        self,
        google_keep_name: str,
        clear_after: bool = False,
        img_style: str = CSS_MEDIUM,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.clear_after = clear_after
        self.img_style = img_style
        self.keep = GoogleKeep(SENDER_EMAIL, SENDER_PASSWORD, google_keep_name)

    def generate_content(self) -> str:
        images = map(
            lambda link: html_img(url=link, style=self.img_style),
            self.keep.get_note_imgs(),
        )
        return html_from_txt(f"{self.keep.get_note_txt()}\n{''.join(images)}")

    def on_email_sent(self):
        if self.clear_after:
            self.keep.clear_note()
            if len(self.keep.get_note_imgs()) > 0:
                seq = int(self.keep._get_note().title[len(self.title) :])
                self.keep.create_note(f"{self.title}{seq + 1}", "")
