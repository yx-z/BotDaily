import logging
import traceback
from datetime import datetime
from typing import List

from feature.base import Feature
from mail.subject import Subject
from utility.constant import HTML_NEW_LINE, CSS_DEFAULT_DIV
from utility.html_builder import html_div


# if "all" in test_next_day_feature: test all
TEST_ALL = "all"


class Recipient:
    def __init__(
        self,
        email_address: str,
        subject: Subject,
        features: List[Feature],
        div_style: str = CSS_DEFAULT_DIV,
        test_next_day_feature: List[str] = None,
    ):
        self.email_address = email_address
        self.subject = subject
        self.div_style = div_style
        self.features = features
        self.test_next_day_feature = test_next_day_feature
        self.current_date_time = None  # lazy initialization by set_current_date_time

    def set_current_date_time(self, current_date_time: datetime):
        self.current_date_time = current_date_time
        self.subject.current_date_time = current_date_time
        for feature in self.features:
            feature.current_date_time = current_date_time

    def generate_subject(self) -> str:
        return self.subject.to_complete_string()

    def generate_body(self, test_filter: bool = False) -> str:
        def generate_feature(feature: Feature) -> str:
            logging.info(f"{feature.get_name()} generating.")
            try:
                generated_html = feature.generate_html()
                return generated_html
            except Exception as exception:
                if test_filter:
                    return f"""Exception: {exception}

Traceback: {traceback.format_exc()}"""
                else:
                    raise exception

        if TEST_ALL in self.test_next_day_feature:
            # TEST_ALL as if no filter, i.e. add all features
            test_filter = False

        return html_div(
            inner_html=HTML_NEW_LINE.join(
                map(
                    generate_feature,
                    filter(
                        lambda f: f.get_name() in self.test_next_day_feature,
                        self.features,
                    )
                    if test_filter
                    else self.features,
                )
            ),
            style=self.div_style,
        )

    def on_email_sent(self):
        for feature in self.features:
            feature.on_email_sent()
