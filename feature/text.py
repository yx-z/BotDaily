from feature.base import Feature


class Text(Feature):

    def __init__(self, text: str, div_style: str = ""):
        super().__init__(div_style)
        self.text = text

    @property
    def title(self) -> str:
        return ""

    def generate_content(self) -> str:
        return self.text
