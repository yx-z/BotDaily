from typing import Optional

import random
from feature import Text
from utility.html_builder import html_from_text
from utility.system import get_resource_path


class ExternalRandomizer(Text):
    def __init__(
        self,
        file_name: str,
        end_of_cycle_line: str = "=====",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.file_path = get_resource_path(file_name)
        self.end_of_cycle_line = end_of_cycle_line

    def generate_content(self) -> str:
        self.text = open(self.file_path, "r").readline()[:-1]
        return super().generate_content()

    def on_email_sent(self):
        with open(self.file_path, "w+") as file:
            lines = file.readlines()
            lines.append(lines.pop())
            if lines[0] == self.end_of_cycle_line:
                lines = lines[1:]
                random.shuffle(lines)
                lines.append(self.end_of_cycle_line)
            file.truncate(0)
            file.writelines(lines)


class RandomEnd(ExternalRandomizer):
    def __init__(
        self,
        file_name: str,
        sender_name: str,
        end_of_cycle_line: str = "=====",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__(file_name, end_of_cycle_line, div_style, title)
        self.sender_name = sender_name

    def generate_content(self) -> str:
        return html_from_text(
            f"""
-----
祝{super().generate_content()}的一天。

你的 {self.sender_name}
"""
        )
