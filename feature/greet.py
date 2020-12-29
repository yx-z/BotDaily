from datetime import datetime
from typing import Optional

from feature.txt import Txt
from utility.constant import DATE_FORMAT


class Greet(Txt):
    def __init__(
        self,
        recipient_name: str,
        start_date: Optional[str] = None,
        commit_date: Optional[str] = None,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.recipient_name = recipient_name
        self.start_date = (
            None if start_date is None else datetime.strptime(start_date, DATE_FORMAT)
        )
        self.commit_date = (
            None if commit_date is None else datetime.strptime(commit_date, DATE_FORMAT)
        )
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        self.txt = ""
        if self.start_date is not None:
            self.txt += f"初见{self.recipient_name}的第{self._get_days(self.start_date)}天, "
        if self.commit_date is not None:
            self.txt += f"再见倾心的第{(self._get_days(self.commit_date))}天, "

        hour = self.current_date_time.hour
        if hour in range(5, 13):
            phase = "早"
        elif hour in range(13, 19):
            phase = "午"
        else:
            phase = "晚"
        self.txt += f"{phase}安~"

        return super().generate_content()

    def _get_days(self, dt: datetime) -> int:
        return (self.current_date_time - dt).days + 1
