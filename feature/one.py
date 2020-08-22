from typing import List

from feature.base import Feature


class One(Feature):

    @property
    def title(self) -> str:
        return "ONE·一个"

    # `includes` is a sublist of ["cover", "quote", "article", "question"]
    def __init__(self, includes: List[str], image_style: str = "",
                 div_style: str = ""):
        super().__init__(div_style)
        self.includes = list(map(lambda t: t.lower(), includes))
        self.image_style = image_style

    def generate_content(self) -> str:
        pass
