import scrapy


class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath('//div[@class="quote"]'):
            item = {
                # author_name can use this xpath also (".//small[@class='author']/text()")
                'author_name': quote.xpath("descendant::small[@class='author']/text()").extract_first(),
                # text can use this xpath also ("span[@class='text']/text()") or ("./span[@class='text']/text()")
                'text': quote.xpath("child::span[@class='text']/text()").extract_first(),
                'tags': quote.xpath('./div/a/text()').extract(),
            }
            yield item
