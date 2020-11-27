from typing import Optional

from feature.text import Text
from utility.system import get_resource_path
from utility.html_builder import *
from utility.constant import *


class ExternalText(Text):
    def __init__(
            self,
            text_file: str,
            as_python: bool = False,
            clear_after: bool = False,
            div_style: str = "",
            title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.text_file = text_file
        self.clear_after = clear_after
        self.as_python = as_python

    def generate_content(self) -> str:
        with open(get_resource_path(self.text_file), "r+") as file:
            self.text = file.read()
            if self.as_python:
                self.text = eval(self.text)
            return super().generate_content()

    def on_email_sent(self):
        if self.clear_after:
            with open(get_resource_path(self.text_file), "w+") as file:
                file.truncate(0)
                if self.as_python:
                    file.write(
                        '''# html_tag(name: str, paired: bool = False, inner_html: str = "", **kwargs)
# html_img(url: Optional[str] = None, path: str = "", style: str = "", **kwargs)
# html_div(inner_html: str, style: str = "", **kwargs)
# html_emphasis(text: str, bold: bool = True, italic: bool = True)
# html_a(text: str, url: str, style: str = "", **kwargs)
# css_build(*styles: str, **kw_styles)
# HTML_NEW_LINE = "<br>"
# HTML_LESS_THAN_TEXT = "&lt;"
# HTML_GREATER_THAN_TEXT = "&gt;"

# CSS_DEFAULT_DIV = "font-size: 1.15em; color: #000; padding: 5px;"
# CSS_FULL_WIDTH = "width: 100%;"
# CSS_CENTER = "text-align: center;"
# CSS_BIG = "display: block; width: 90%; margin: auto;"
# CSS_MEDIUM = "display: block; width: 60%; margin: auto;"
# CSS_SMALL = "display: block; width: 40%; margin: auto;"

f"""

"""
'''
                    )
