import copy
import logging
from datetime import datetime
from typing import List

from feature.base import Feature
from mail.subject import Subject
from utility.constant import HTML_NEW_LINE


class Recipient:

    def __init__(self, email_address: str, current_date_time: datetime,
                 subject: Subject, features: List[Feature],
                 div_style: str = ""):
        self.email_address = email_address

        self.current_date_time = current_date_time

        subject.current_date_time = current_date_time
        self.subject = subject

        for feature in features:
            feature.current_date_time = current_date_time
        self.features = features

        self.div_style = div_style

    def generate_subject(self) -> str:
        return self.subject.to_complete_string()

    def generate_body(self) -> str:
        def generate_feature(feature: Feature) -> str:
            generated_html = feature.generate_html()
            logging.info(f"{type(feature).__name__} generated.")
            return generated_html

        return f"<div style='{self.div_style}'>{HTML_NEW_LINE.join(map(lambda f: generate_feature(f), self.features))}</div>"

    def copy(self):
        return copy.deepcopy(self)
