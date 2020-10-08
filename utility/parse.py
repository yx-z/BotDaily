from datetime import datetime

import pdfkit as pdfkit


def string_to_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d")


def date_to_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m-%d")


def month_to_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m")


PARSE_ANGLE_BRACKETS = "parse_angle_brackets"
PARSE_NEW_LINE = "parse_NEW_LINE"


def text_to_html(text: str, *args) -> str:
    parsed = text
    # process order matters, not the order of args
    if PARSE_ANGLE_BRACKETS in args:
        parsed = parsed.replace("<", "&lt;").replace(">", "&gt;")
    if PARSE_NEW_LINE in args:
        parsed = parsed.replace("\n", "<br>")
    return parsed


def html_to_pdf(in_path: str, out_path: str) -> bool:
    return pdfkit.from_file(in_path, out_path, options={"encoding": "utf-8"})
