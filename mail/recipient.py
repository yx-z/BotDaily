import copy
from datetime import datetime
from typing import List

from feature.base import Feature
from feature.subject import Subject
from utility.constant import HTML_NEW_LINE


class Recipient:

    def __init__(self, email_address: str, current_date_time: datetime,
                 subject: Subject, features: List[Feature]):
        self.email_address = email_address

        self.current_date_time = current_date_time

        subject.current_date_time = current_date_time
        self.subject = subject

        for feature in self.features:
            feature.current_date_time = current_date_time
        self.features = features

    def generate_subject(self) -> str:
        return self.subject.to_complete_string()

    def generate_body(self) -> str:
        return HTML_NEW_LINE.join(map(lambda feature: feature.generate_body(),
                                      self.features))

    def copy(self):
        return copy.deepcopy(self)
