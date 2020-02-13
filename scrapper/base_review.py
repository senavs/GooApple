import re
from abc import ABC, abstractmethod
from typing import List

from scrapper.scrapper import Scrapper


class BaseReviewScrapper(ABC):
    RE_ASSERT_URL = r'^https://base.com'

    def __init__(self, url: str, drive_path: str = None, waiter_timeout: int = 3, options: List[str] = None):
        assert re.findall(self.RE_ASSERT_URL, url), f'URL like {self.RE_ASSERT_URL} is required'

        self.url = url
        self.driver = Scrapper(drive_path, waiter_timeout, options)

    @staticmethod
    def to_dict(**kwargs) -> dict:
        return dict(**kwargs)

    @abstractmethod
    def run(self, n: int, output_file: str):
        pass
