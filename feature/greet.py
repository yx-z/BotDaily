from datetime import datetime

from feature.text import Text


class Greet(Text):

    def __init__(self, recipient_name: str,
                 know_date_time: datetime = None):
        super().__init__("")
        self.recipient_name = recipient_name
        self.know_date_time = know_date_time

    def generate_html(self) -> str:
        hour = self.current_date_time.hour
        if hour in range(5, 13):
            phase = "早"
        elif hour in range(13, 19):
            phase = "午"
        else:
            phase = "晚"

        if self.know_date_time is None:
            self.text = f"{self.recipient_name}{phase}安~"
            return super().generate_html()
        else:
            self.text = f"遇见{self.recipient_name}的第{(self.current_date_time - self.know_date_time).days}天，{phase}安~"
            return super().generate_html()
