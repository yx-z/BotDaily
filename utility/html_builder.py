from utility.constant import (
    HTML_LESS_THAN_TEXT,
    HTML_GREATER_THAN_TEXT,
    HTML_NEW_LINE,
    HTML_SINGLE_QUOTE,
    CSS_MEDIUM,
)
from utility.img import upload_img
from typing import Optional, List

from utility.system import get_res_path


def html_from_txt(
    txt: str, parse_list: List[str] = None, exclude_parse_list: List[str] = None
) -> str:
    parsed_txt = txt

    if parse_list is None:
        # default parse_list
        parse_list = ["\n"]
    if exclude_parse_list is None:
        exclude_parse_list = []

    def need_parse(symbol: str) -> bool:
        if parse_list is not None:
            return symbol in parse_list
        return symbol not in exclude_parse_list

    # the following process order matters
    if need_parse("<"):
        parsed_txt = parsed_txt.replace("<", HTML_LESS_THAN_TEXT)
    if need_parse(">"):
        parsed_txt = parsed_txt.replace(">", HTML_GREATER_THAN_TEXT)
    if need_parse("'"):
        parsed_txt = parsed_txt.replace("'", HTML_SINGLE_QUOTE)
    if need_parse("\n"):
        parsed_txt = parsed_txt.replace("\n", HTML_NEW_LINE)
    return parsed_txt


def html_tag(name: str, paired: bool = False, inner_html: str = "", **kwargs) -> str:
    attributes = " ".join(map(lambda p: f"{p[0]}='{p[1]}'", kwargs.items()))
    if paired:
        return f"<{name} {attributes}>{inner_html}</{name}>"
    else:
        return f"<{name} {attributes}>"


def html_img(
    url: Optional[str] = None,
    file_name: Optional[str] = None,
    style: str = CSS_MEDIUM,
    **kwargs,
) -> str:
    if url is None:
        url = upload_img(get_res_path(file_name))
    return html_tag("img", False, src=url, style=style, **kwargs)


def html_div(inner_html: str, style: str = "", **kwargs) -> str:
    return html_tag("div", True, inner_html, style=style, **kwargs)


def html_emphasis(text: str, bold: bool = True, italic: bool = True) -> str:
    html = text
    if bold:
        html = html_tag("b", True, html)
    if italic:
        html = html_tag("i", True, html)
    return html


def html_a(text: str, url: str, style: str = "", **kwargs) -> str:
    return html_tag("a", True, text, href=url, style=style, **kwargs)
