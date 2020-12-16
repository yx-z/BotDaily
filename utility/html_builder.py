from utility.constant import HTML_LESS_THAN_TEXT, HTML_GREATER_THAN_TEXT, HTML_NEW_LINE, HTML_SINGLE_QUOTE
from utility.image import upload_image
from typing import Optional, List

from utility.system import get_resource_path


def html_from_text(text: str, exclude_parse_list: List[str] = None) -> str:
    parsed = text
    not_exclude = lambda s: s not in exclude_parse_list
    # the following process order matters
    if not_exclude("<"):
        parsed = parsed.replace("<", HTML_LESS_THAN_TEXT)
    if not_exclude(">"):
        parsed = parsed.replace(">", HTML_GREATER_THAN_TEXT)
    if not_exclude("'"):
        parsed = parsed.replace("'", HTML_SINGLE_QUOTE)
    if not_exclude("\n"):
        parsed = parsed.replace("\n", HTML_NEW_LINE)
    return parsed


def html_tag(name: str, paired: bool = False, inner_html: str = "", **kwargs) -> str:
    attributes = " ".join(map(lambda p: f"{p[0]}='{p[1]}'", kwargs.items()))
    if paired:
        return f"<{name} {attributes}>{inner_html}</{name}>"
    else:
        return f"<{name} {attributes}>"


def html_img(
        url: Optional[str] = None,
        file_name: Optional[str] = None,
        style: str = "",
        **kwargs,
) -> str:
    if url is None:
        url = upload_image(get_resource_path(file_name))
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
