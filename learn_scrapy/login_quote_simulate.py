import scrapy


class LoginQuoteSimulateSpider(scrapy.Spider):
    name = 'login-quote-simulate'
    allowed_domains = ['toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        return scrapy.FormRequest.from_response(
            response,
            formdata={'username': 'abc', 'password': 'abc'},
            callback=self.parse_quotes
        )

    def parse_quotes(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'author_url': quote.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first(),
            }
