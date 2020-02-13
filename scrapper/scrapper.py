from typing import Union, List

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.enums import ScrollEnum


class Scrapper:

    def __init__(self, driver_path: str = None, waiter_timeout: int = 3, options: List[str] = None):
        """Base class to WebScrapper with selenium

        :param driver_path: web drive file path
            :type: str
            :tip: if driver_path is none, FireFox web drive will be used
        :param waiter_timeout: general wait timeout
            :type: int
        :param options: driver config
             :type: List[str]
        """

        # selecting driver
        if not driver_path:
            driver = webdriver.Firefox
            driver_options = FireFoxOptions()
        else:
            driver = webdriver.Chrome
            driver_options = ChromeOptions()

        # add config
        if options:
            for option in options:
                driver_options.add_argument(option)

        self.driver = driver(driver_path, options=driver_options)
        self.waiter = WebDriverWait(self.driver, waiter_timeout)

    def __enter__(self) -> 'Scrapper':
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.driver.close()

    def get(self, url: str):
        """Access the web page

        :param url: page url
            :type: str
        """

        self.driver.get(url)

    def find_element_by_xpath(self, xpath: str) -> Union[WebElement, None]:
        """Find the element

        :param xpath: html full xpath
        :return: web element
            :type: WebElement or None if not found
        """
        try:
            element = self.driver.find_element_by_xpath(xpath)
        except NoSuchElementException:
            return None
        else:
            return element

    def wait_find_element_by_xpath(self, xpath: str) -> Union[WebElement, None]:
        """Wait and find the element

        :param xpath: html full xpath
        :return: web element
            :type: WebElement or None if not found
        """

        try:
            element = self.waiter.until(EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            return None
        else:
            return element

    def scroll_page(self, where: str, direction: ScrollEnum):
        """ Scroll the page UP or DOWN

        :param where: base xpath
            :type: str
            :tip: to scroll all the page, use /html/body
        :param direction: scroll up or down
            :type: ScrollEnum
        """

        element = self.find_element_by_xpath(where)
        if element:
            if direction == ScrollEnum.UP:
                element.send_keys(Keys.HOME)
            elif direction == ScrollEnum.DOWN:
                element.send_keys(Keys.END)

    def js_command(self, command: str, element: WebElement):
        """Execute JavaScript command in an element

        :param command: js command
            :type: str
        :param element: element which will be apply the command
             :type: WebElement
        """

        self.driver.execute_script('arguments[0]' + command, element)
