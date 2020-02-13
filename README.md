# GooApple
Review scrapper from Google Play and Apple Store

## About
Python scrapper to extract and save reviews from apps in Google Play or Apple Store.

## Usage
### Google reviews scrapper
```python
from scrapper.google import GoogleReviewScrapper

URL_GOOGLE = 'https://play.google.com/store/apps/details?id=br.com.bb.android&hl=pt-br&showAllReviews=true'
OPTIONS = ['--headless']

scrapper = GoogleReviewScrapper(URL_GOOGLE, options=OPTIONS)
```

### Apple reviews scrapper
```python
from scrapper.apple import AppleReviewScrapper

URL_APPLE = 'https://apps.apple.com/br/app/banco-do-brasil/id330984271#see-all/reviews'
OPTIONS = ['--headless']

scrapper = AppleReviewScrapper(URL_APPLE, options=OPTIONS)
```

The ``OPTIONS`` variables are from [selenium webdriver config](!https://selenium-python.readthedocs.io/api.html).

### Running
The first argument indicates how many data it'll extract and, the second one, it's here the data will be saved.
```python
scrapper.run(20000, './output.csv')
```
