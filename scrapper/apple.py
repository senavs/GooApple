from utils.enums import ScrollEnum
from utils.context_csv import CSVCustom
from scrapper.base import BaseReviewScrapper


class AppleReviewScrapper(BaseReviewScrapper):
    RE_ASSERT_URL = '^https://apps.apple.com'

    CARD_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]'
    NAME_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]/div/span[1]'
    DATE_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]/div/time'
    STAR_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]/figure'
    TITLE_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]/h3'
    DESCRIPTIONS_XPATH = r'/html/body/div[4]/div/main/div/div/div/section/div[2]/div[{}]/div[2]/blockquote/div'

    def run(self, n: int, output_file: str):
        """ Execute the scrapper and save all data in a csv file

        :param n: how many data to be extracted
            :type: int
        :param output_file: csv file path where data will be saved
            :type: str
        """

        with self.driver as web:
            web.get(self.url)

            with CSVCustom(output_file, ['name', 'date', 'title', 'star', 'description']) as csv:

                not_found = 0
                for i in range(1, n + 1):
                    # find card element
                    if web.wait_find_element_by_xpath(self.CARD_XPATH.format(i)):
                        # resetting not_found counter
                        not_found = 0
                        # getting all web elements
                        name = web.find_element_by_xpath(self.NAME_XPATH.format(i)).text
                        date = web.find_element_by_xpath(self.DATE_XPATH.format(i)).text
                        star = web.find_element_by_xpath(self.STAR_XPATH.format(i)).get_attribute('aria-label')
                        title = web.find_element_by_xpath(self.TITLE_XPATH.format(i)).text
                        descriptions_element = web.find_element_by_xpath(self.DESCRIPTIONS_XPATH.format(i))
                        description = '\n'.join([description.text for description in descriptions_element.find_elements_by_tag_name('p')])
                        # data to dict
                        data = self.to_dict(name=name, date=date, star=star, title=title, description=description)
                        # saving to csv file
                        csv.write_row(data)
                    else:
                        # scroll the page up to unsure that the page will load more data
                        web.scroll_page('/html', ScrollEnum.UP)
                        # increment 1
                        not_found += 1

                    # if not found 4 sequence elements, stop
                    if not_found == 5:
                        break

                    # scroll down the page to load more data
                    web.scroll_page('/html', ScrollEnum.DOWN)
