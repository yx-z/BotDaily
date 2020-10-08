from datetime import datetime

import pdfkit as pdfkit


def string_to_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d")


def date_to_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m-%d")


def month_to_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m")


def text_to_html(text: str, parse_angle_brackets: bool = True,
                 parse_new_line: bool = True) -> str:
    parsed = text
    # process order matters
    if parse_angle_brackets:
        parsed = parsed.replace("<", "&lt;").replace(">", "&gt;")
    if parse_new_line:
        parsed = parsed.replace("\n", "<br>")
    return parsed


def html_to_pdf(in_path: str, out_path: str) -> bool:
    return pdfkit.from_file(in_path, out_path, options={"encoding": "utf-8"})
