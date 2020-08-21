from feature.base import Feature


class Text(Feature):

    def __init__(self, text: str):
        self.text = text

    @property
    def title(self) -> str:
        return ""

    def generate_html(self) -> str:
        return self.text.replace("\n", "<br>")
