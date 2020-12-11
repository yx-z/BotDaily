import json
import logging
from datetime import datetime
from typing import List, Optional

import requests
from bs4 import BeautifulSoup

from feature.base import Feature
from utility.constant import DATE_FORMAT
from utility.system import get_resource_path
from utility.html_builder import html_img, html_div, html_a, html_tag

HEADER = {
    "Host": "www.zhihu.com",
    "Referer": "https://www.zhihu.com/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36"
    " (KHTML, like Gecko) Chrome/56.0.2924.87",
}


class ZhihuStory(Feature):
    def __init__(
        self,
        file_name: str,
        start_date_time: str,
        avatar_style: str = "border-radius: 50%; width: 64px;",
        div_style: str = "",
        title: Optional[str] = "知乎收录",
    ):
        super().__init__(div_style, title)
        self.file_path = get_resource_path(file_name)
        self.start_date_time = datetime.strptime(start_date_time, DATE_FORMAT)
        self.avatar_style = avatar_style
        self.current_date_time = None  # lazy initialization by Recipient class

    def generate_content(self) -> str:
        index = max(0, (self.current_date_time - self.start_date_time).days)
        logging.info(f"Zhihu Index: {index}")
        answer_url = open(self.file_path, "r").readlines()[index]
        logging.info(f"Zhihu Answer URL: {answer_url}")
        return self._request_answer(answer_url)

    def _request_answer(self, answer_url: str) -> str:
        answer_id = answer_url[answer_url.rfind("/") + 1 :]
        api_url = f"https://www.zhihu.com/api/v4/answers/{answer_id}?include=content"
        response = requests.get(api_url, headers=HEADER).json()
        content = response["content"]
        content = content.replace("<noscript>", "").replace("</noscript>", "")
        soup = BeautifulSoup(content, "html.parser")
        for tag in soup.find_all(lambda t: "data-actualsrc" in t.attrs):
            tag.extract()
        for tag in soup.find_all("p", {"class": "ztext-empty-paragraph"}):
            tag.extract()
        for tag in soup.find_all("img"):
            tag["style"] = "width:95%;"
            if "data-original" in tag.attrs:
                del tag["data-original"]
            if "data-rawheight" in tag.attrs:
                del tag["data-rawheight"]
            if "data-rawwidth" in tag.attrs:
                del tag["data-rawwidth"]
            if "class" in tag.attrs:
                del tag["class"]
            if "width" in tag.attrs:
                del tag["width"]
        for fig in soup.find_all("figure"):
            fig.attrs.clear()
        str_soup = str(soup)
        return f"""{html_tag(name="h3", paired=True, inner_html=response["question"]["title"])}
{html_img(url=response["author"]["avatar_url"], style=self.avatar_style)}
作者: {response["author"]["name"]}
<br>
{html_div(inner_html=str_soup)}
<br>
{html_a(text="知乎原文", url=answer_url)}
"""

    # ON HOLD, NOT IN USE
    @staticmethod
    def _request_answer_by_question(qid, total=10, page_num=0, limit=10) -> List:
        answers = []
        count = 0
        while True:
            url = (
                "https://www.zhihu.com/api/v4/questions/"
                + str(qid)
                + "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closedsfd_comment%2Creward_info"
                "%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason"
                "%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment"
                "%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings"
                "%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info"
                "%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized"
                "%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D"
                ".mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A"
                "%5D.topics&limit="
                + str(limit)
                + "&offset="
                + str(page_num * limit)
                + "&platform=desktop&sort_by=default"
            )
            req = requests.get(url, headers=HEADER)
            res_json = json.loads(req.text)
            data = res_json["data"]
            page_num += 1
            for item in data:
                count += 1
                if count > total:
                    return answers
                else:
                    title = item["question"]["title"]
                    author = item["author"]["name"]
                    content = (
                        item["content"]
                        .replace("<noscript>", "")
                        .replace("</noscript>", "")
                        .replace('<img src="data:image/svg+xml', '<meta src="')
                    )
                    # further use title, author, content here
                    # ...
            if res_json["paging"]["is_end"] or count >= res_json["paging"]["totals"]:
                break
        return answers
