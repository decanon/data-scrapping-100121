from scrapy.loader import ItemLoader
from js_scrapy.items import QuoteItem
import scrapy


class QuotesCleanSpider(scrapy.Spider):
    name = 'quotes_clean'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            loader = ItemLoader(item=QuoteItem(), selector=quote, response=response)
            loader.add_xpath('author', "descendant::small[@class='author']/text()")
            loader.add_xpath('text', "child::span[@class='text']/text()")
            loader.add_xpath('tags', './div/a/text()')
            yield loader.load_item()
