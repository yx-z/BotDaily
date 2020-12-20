from typing import Optional

import random
from feature import Txt
from utility.system import get_res_path, clear_file


class ExtRand(Txt):
    def __init__(
        self,
        file_name: str,
        end_of_cycle_line: str = "=====",
        div_style: str = "",
        title: Optional[str] = None,
    ):
        super().__init__("", div_style, title)
        self.file_path = get_res_path(file_name)
        self.end_of_cycle_line = end_of_cycle_line

    def generate_content(self) -> str:
        with open(self.file_path, "r") as file:
            self.text = ExtRand.ignore_new_line(file.readline())
        return super().generate_content()

    def on_email_sent(self):
        # cannot clear_file() when file is opened, needs to open separate for read and write
        with open(self.file_path, "r") as file:
            lines = list(map(ExtRand.ignore_new_line, file.readlines()))
        lines.append(lines.pop(0))
        if lines[0] == self.end_of_cycle_line:
            lines = lines[1:]
            random.shuffle(lines)
            lines.append(self.end_of_cycle_line)
        clear_file(self.file_path)
        with open(self.file_path, "w") as file:
            file.writelines(list(map(ExtRand.append_new_line, lines)))

    @staticmethod
    def ignore_new_line(string: str) -> str:
        return string.replace("\n", "")

    @staticmethod
    def append_new_line(string: str) -> str:
        return f"{string}\n"
