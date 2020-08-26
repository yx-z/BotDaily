from datetime import datetime
from typing import Optional

from feature.base import Feature


class Greet(Feature):

    def __init__(self, recipient_name: str,
                 start_date_time: datetime = None, div_style: str = "",
                 title: Optional[str] = None):
        super().__init__(div_style, title)
        self.recipient_name = recipient_name
        self.know_date_time = start_date_time
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        hour = self.current_date_time.hour
        if hour in range(5, 13):
            phase = "早"
        elif hour in range(13, 19):
            phase = "午"
        else:
            phase = "晚"

        if self.know_date_time is None:
            return f"{self.recipient_name}{phase}安~"
        else:
            return f"遇见{self.recipient_name}的第{(self.current_date_time - self.know_date_time).days + 1}天，{phase}安~"
