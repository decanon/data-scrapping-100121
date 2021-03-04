import scrapy
from scrapy_selenium import SeleniumRequest


class QuotesJsSpider(scrapy.Spider):
    name = 'quotes_js'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    def start_requests(self):
        yield SeleniumRequest(url='http://quotes.toscrape.com/js/', callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract(),
            }
            yield item

        # driver = response.request.meta['driver']
        # driver.find_elements_by_css_selector('li.next > a')[0].click()
        # time.sleep(2)
        # print(f'URL NOW: {driver.current_url}' )
