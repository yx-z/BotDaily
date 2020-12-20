from abc import abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup

from feature.base import Feature
from utility.constant import CSS_MEDIUM, CSS_CENTER


class One(Feature):
    def __init__(
        self,
        img_style: str = "",
        div_style: str = "",
        title: Optional[str] = "ONE·一个",
    ):
        super().__init__(div_style, title)
        self.img_style = img_style

    @staticmethod
    def _get_soup(url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "html.parser")

    @staticmethod
    def _get_home() -> BeautifulSoup:
        return One._get_soup("http://www.wufazhuce.com/")

    @abstractmethod
    def generate_content(self) -> str:
        pass


class OneCover(One):
    def __init__(
        self,
        img_style: str = CSS_MEDIUM,
        div_style: str = "",
        title: Optional[str] = "One·一个",
    ):
        super().__init__(img_style, div_style, title)

    def generate_content(self) -> str:
        img = One._get_home().find("img", class_="fp-one-imagen")
        img["style"] = self.img_style
        return str(img)


class OneQuote(One):
    def __init__(
        self, img_style: str = "", div_style: str = CSS_CENTER, title: Optional[str] = None
    ):
        super().__init__(img_style, div_style, title)

    def generate_content(self) -> str:
        return One._get_home().find("div", class_="fp-one-cita").text.strip()


class OneArticle(One):
    def __init__(
        self, img_style: str = "", div_style: str = "", title: Optional[str] = None
    ):
        super().__init__(img_style, div_style, title)

    def generate_content(self) -> str:
        p = One._get_home().find("p", class_="one-articulo-titulo")
        article_url = p.find("a")["href"]
        soup = One._get_soup(article_url)
        quote = soup.find("div", class_="comilla-cerrar").text.strip()
        title = soup.find("h2", class_="articulo-titulo").text.strip()
        author = soup.find("p", class_="articulo-autor").text.strip()[3:]
        text = soup.find("div", class_="articulo-contenido").get_text(separator="\n")
        return f"""{title} - {author}
{quote}
{text}

"""


class OneQuestionAnswer(One):
    def generate_content(self) -> str:
        p = One._get_home().find("p", class_="one-cuestion-titulo")
        qa_url = p.find("a")["href"]
        soup = One._get_soup(qa_url)
        q = soup.find("div", class_="cuestion-contenido").text.strip()
        a = (
            soup.find_all("div", class_="cuestion-contenido")[-1]
            .get_text(separator="\n")
            .strip()
        )
        return f"""问: {q}
答:
{a}
"""
