from feature.base import Feature


class Text(Feature):

    def __init__(self, text: str, title: str = "", div_style: str = ""):
        super().__init__(div_style)
        self.text = text
        self.__header_title__ = title

    @property
    def title(self) -> str:
        return self.__header_title__

    def generate_content(self) -> str:
        return self.text
