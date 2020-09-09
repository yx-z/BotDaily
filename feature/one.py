from abc import abstractmethod
from typing import Optional

import requests
from bs4 import BeautifulSoup

from feature.base import Feature


class One(Feature):

    def __init__(self, image_style: str = "", div_style: str = "",
                 title: Optional[str] = "ONE·一个"):
        super().__init__(div_style, title)
        self.image_style = image_style

    @staticmethod
    def __get_soup__(url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "html.parser")

    @staticmethod
    def __get_home__() -> BeautifulSoup:
        return One.__get_soup__("http://www.wufazhuce.com/")

    @abstractmethod
    def generate_content(self) -> str:
        pass


class OneCover(One):

    def generate_content(self) -> str:
        img = One.__get_home__().find("img", class_="fp-one-imagen")
        img["style"] = self.image_style
        return str(img)


class OneQuote(One):
    def generate_content(self) -> str:
        return One.__get_home__().find("div", class_="fp-one-cita").text.strip()


class OneArticle(One):

    def generate_content(self) -> str:
        p = One.__get_home__().find("p", class_="one-articulo-titulo")
        article_url = p.find("a")["href"]
        soup = One.__get_soup__(article_url)
        quote = soup.find("div", class_="comilla-cerrar").text.strip()
        title = soup.find("h2", class_="articulo-titulo").text.strip()
        author = soup.find("p", class_="articulo-autor").text.strip()[3:]
        text = soup.find("div", class_="articulo-contenido").get_text(
                separator="\n")
        return f"""{title} - {author}
{quote}
{text}

"""


class OneQuestionAnser(One):
    def generate_content(self) -> str:
        p = One.__get_home__().find("p", class_="one-cuestion-titulo")
        qa_url = p.find("a")["href"]
        soup = One.__get_soup__(qa_url)
        q = soup.find("div", class_="cuestion-contenido").text.strip()
        a = soup.find_all("div", class_="cuestion-contenido")[-1].get_text(
                separator="\n").strip()
        return f"""问: {q}
答:
{a}
"""
