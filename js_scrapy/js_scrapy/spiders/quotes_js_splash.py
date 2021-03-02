import scrapy
from scrapy_splash import SplashRequest


class QuotesJsSplashSpider(scrapy.Spider):
    name = 'quotes_js_splash'

    def start_requests(self):
        yield SplashRequest(url='http://quotes.toscrape.com/js/', callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
            }
            yield item
