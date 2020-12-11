from datetime import datetime
from typing import Optional

from feature.text import Text
from utility.constant import DATE_FORMAT


class Greet(Text):
    def __init__(
        self,
        recipient_name: str,
        start_date: Optional[str] = None,
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.recipient_name = recipient_name
        self.start_date = (
            datetime.strptime(start_date, DATE_FORMAT)
            if start_date is not None
            else None
        )
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        hour = self.current_date_time.hour
        if hour in range(5, 13):
            phase = "早"
        elif hour in range(13, 19):
            phase = "午"
        else:
            phase = "晚"

        if self.start_date is None:
            self.text = f"{self.recipient_name}{phase}安~"
        else:
            self.text = f"遇见{self.recipient_name}的第{(self.current_date_time - self.start_date).days + 1}天，{phase}安~"
        return super().generate_content()
