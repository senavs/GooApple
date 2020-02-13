import re
from abc import ABC, abstractmethod
from typing import List

from scrapper.scrapper import Scrapper


class BaseReviewScrapper(ABC):
    RE_ASSERT_URL = r'^https://base.com'

    def __init__(self, url: str, drive_path: str = None, waiter_timeout: int = 3, options: List[str] = None):
        """Base class to Store Review scrapper

        :param url: url with all reviews
            :type: str
        :param drive_path: chrome/firefox driver file path
            :type: str
        :param waiter_timeout: general wait timeout
            :type: int
        :param options:driver config
             :type: List[str]
        """

        assert re.findall(self.RE_ASSERT_URL, url), f'URL like {self.RE_ASSERT_URL} is required'

        self.url = url
        self.driver = Scrapper(drive_path, waiter_timeout, options)

    @staticmethod
    def to_dict(**kwargs) -> dict:
        """To dict object"""

        return dict(**kwargs)

    @abstractmethod
    def run(self, n: int, output_file: str):
        """ Execute the scrapper and save all data in a csv file

        :param n: how many data to be extracted
            :type: int
        :param output_file: csv file path where data will be saved
            :type: str
        """
