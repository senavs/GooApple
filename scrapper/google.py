from utils.enums import ScrollEnum
from utils.context_csv import CSVCustom
from scrapper.base import BaseReviewScrapper


class GoogleReviewScrapper(BaseReviewScrapper):
    RE_ASSERT_URL = '^https://play.google.com/'

    CARD_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{}]'
    NAME_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{}]/div/div[2]/div[1]/div[1]/span'
    DATE_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[1]/div[{}]/div/div[2]/div[1]/div[1]/div/span[2]'
    STAR_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{}]/div/div[2]/div[1]/div[1]/div/span[1]/div/div'
    READ_FULL_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{}]/div/div[2]/div[2]/span[1]/div/button'
    DESCRIPTION_SHORT_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{}]/div/div[2]/div[2]/span[1]'
    DESCRIPTION_FULL_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div/div[{}]/div/div[2]/div[2]/span[2]'
    READ_MORE_XPATH = r'/html/body/div[1]/div[4]/c-wiz/div/div[2]/div/div[1]/div/div/div[1]/div[2]/div[2]/div/span/span'

    def run(self, n: int, output_file: str):
        """ Execute the scrapper and save all data in a csv file

        :param n: how many data to be extracted
            :type: int
        :param output_file: csv file path where data will be saved
            :type: str
        """

        with self.driver as web:
            web.get(self.url)

            with CSVCustom(output_file, ['name', 'date', 'star', 'description']) as csv:

                not_found = 0
                for i in range(1, n + 1):
                    print(i)
                    # not found 5 time in a row the READ MORE element
                    if not_found == 5:
                        break
                    # find card element
                    if web.wait_find_element_by_xpath(self.CARD_XPATH.format(i + 2)):
                        # resetting not_found counter
                        not_found = 0
                        # getting all web elements
                        name = web.find_element_by_xpath(self.NAME_XPATH.format(i)).text
                        star = web.find_element_by_xpath(self.STAR_XPATH.format(i)).get_attribute('aria-label')
                        date = web.find_element_by_xpath(self.DATE_XPATH.format(i)).text
                        if web.find_element_by_xpath(self.READ_FULL_XPATH.format(i)):
                            description = web.find_element_by_xpath(self.DESCRIPTION_FULL_XPATH.format(i)).get_attribute('textContent')
                        else:
                            description = web.find_element_by_xpath(self.DESCRIPTION_SHORT_XPATH.format(i)).text
                        # to dict
                        data = self.to_dict(name=name, date=date, star=star, description=description)
                        # saving to file
                        csv.write_row(data)
                    else:
                        # increment 1 to not_found to break the loop the is the end
                        not_found += 1
                        # clicking to the button read more to load more data
                        read_more = web.find_element_by_xpath(self.READ_MORE_XPATH)
                        if read_more:
                            web.js_command('.click()', read_more)

                    # scrolling the page down
                    web.scroll_page('/html', ScrollEnum.DOWN)
