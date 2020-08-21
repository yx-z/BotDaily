from datetime import datetime


def string_to_date(date_string: str) -> datetime:
    return datetime.strptime(date_string, "%Y-%m-%d")


def date_to_string(date: datetime) -> str:
    return datetime.strftime(date, "%Y-%m-%d")
