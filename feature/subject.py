class Subject:

    def __init__(self, title: str):
        self.title = title

    def to_complete_string(self) -> str:
        return f"{self.current_date_time.month}/{self.current_date_time.day} {self.title}"
