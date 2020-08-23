from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from feature.base import Feature


class One(Feature):

    # `includes` is a sublist of ["cover", "quote", "article", "question"]
    def __init__(self, includes: List[str], image_style: str = "",
                 div_style: str = "", title: Optional[str] = "ONE·一个"):
        super().__init__(div_style, title)
        self.includes = list(map(lambda t: t.lower(), includes))
        self.image_style = image_style
        self.home = self.__get_soup__("http://www.wufazhuce.com/")

    def __get_soup__(self, url: str) -> BeautifulSoup:
        return BeautifulSoup(requests.get(url).text, "html.parser")

    def generate_content(self) -> str:
        content = ""
        if "cover" in self.includes:
            img = self.home.find("img", class_="fp-one-imagen")
            img["style"] = self.image_style
            content += str(img)
        if "quote" in self.includes:
            content += self.home.find("div", class_="fp-one-cita").text.strip()
        if "article" in self.includes:
            p = self.home.find("p", class_="one-articulo-titulo")
            article_url = p.find("a")["href"]
            soup = self.__get_soup__(article_url)
            quote = soup.find("div", class_="comilla-cerrar").text.strip()
            title = soup.find("h2", class_="articulo-titulo").text.strip()
            author = soup.find("p", class_="articulo-autor").text.strip()[3:]
            text = soup.find("div", class_="articulo-contenido").get_text(
                    separator="\n")
        if "question" in self.includes:
            p = self.home.find("p", class_="one-cuestion-titulo")
            qa_url = p.find("a")["href"]
            soup = self.__get_soup__(qa_url)
            q = soup.find("div", class_="cuestion-contenido").text.strip()
            a = soup.find_all("div", class_="cuestion-contenido")[-1].get_text(
                    separator="\n").strip()
        return content
