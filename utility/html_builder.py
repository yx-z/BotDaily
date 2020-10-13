from utility.constant import HTML_LESS_THAN_TEXT, HTML_GREATER_THAN_TEXT, \
    HTML_NEW_LINE
from utility.image import upload_image


def build_html_from_text(text: str, parse_angle_brackets: bool = True,
                         parse_new_line: bool = True) -> str:
    parsed = text
    # the following process order matters
    if parse_angle_brackets:
        parsed = parsed.replace("<", HTML_LESS_THAN_TEXT).replace(">",
                                                                  HTML_GREATER_THAN_TEXT)
    if parse_new_line:
        parsed = parsed.replace("\n", HTML_NEW_LINE)
    return parsed


def build_html_tag(name: str, paired: bool = False, inner_html: str = "",
                   **kwargs) -> str:
    attributes = " ".join(map(lambda k: f"{k}='{kwargs[k]}'", kwargs.keys()))
    if paired:
        return f"<{name} {attributes}>{inner_html}</{name}>"
    else:
        return f"<{name} {attributes}>"


def build_html_img(image_url: str = None, image_path: str = "",
                   image_style: str = "", **kwargs) -> str:
    if image_url is None:
        image_url = upload_image(image_path)
    return build_html_tag("img", paired=False, src=image_url, style=image_style,
                          **kwargs)


def build_html_div(div_text: str, div_style: str = "", **kwargs) -> str:
    return build_html_tag("div", paired=True, inner_html=div_text,
                          style=div_style, **kwargs)


def build_html_emphasis(text: str, bold: bool = True,
                        italic: bool = True) -> str:
    html = text
    if bold:
        html = build_html_tag("b", True, html)
    if italic:
        html = build_html_tag("i", True, html)
    return html
