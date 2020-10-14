import logging
from datetime import datetime
from typing import List

from feature.base import Feature
from mail.subject import Subject
from utility.constant import HTML_NEW_LINE, CSS_DEFAULT_DIV
from utility.html_builder import html_div


class Recipient:

    def __init__(self, email_address: str,
                 subject: Subject, features: List[Feature],
                 div_style: str = CSS_DEFAULT_DIV,
                 test_next_day_feature_indices: List[int] = None):
        self.email_address = email_address
        self.subject = subject
        self.div_style = div_style
        self.features = features
        self.test_next_day_feature_indices = test_next_day_feature_indices
        self.current_date_time = None  # lazy initialization by set_current_date_time

    def set_current_date_time(self, current_date_time: datetime):
        self.current_date_time = current_date_time
        self.subject.current_date_time = current_date_time
        for feature in self.features:
            feature.current_date_time = current_date_time

    def generate_subject(self) -> str:
        return self.subject.to_complete_string()

    def generate_body(self, test_filter: bool = False) -> str:
        def generate_feature(index: int) -> str:
            feature = self.features[index]
            generated_html = feature.generate_html()
            logging.info(f"{type(feature).__name__} generated.")
            return generated_html

        return html_div(inner_html=HTML_NEW_LINE.join(map(generate_feature,
                                                          self.test_next_day_feature_indices if test_filter else list(
                                                                  range(len(
                                                                          self.features))))),
                        style=self.div_style)

    def on_email_sent(self):
        for feature in self.features:
            feature.on_email_sent()
