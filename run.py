from scrapper.google import GoogleReviewScrapper
from scrapper.apple import AppleReviewScrapper

URL_APPLE = 'https://apps.apple.com/br/app/banco-do-brasil/id330984271#see-all/reviews'
URL_GOOGLE = 'https://play.google.com/store/apps/details?id=br.com.bb.android&hl=pt-br&showAllReviews=true'
DRIVER = '/drivers/chromedriver-70'
OPTIONS = ['--headless']

scrapper = GoogleReviewScrapper(URL_GOOGLE, None, 3, OPTIONS)
scrapper.run(20000, 'test.csv')
