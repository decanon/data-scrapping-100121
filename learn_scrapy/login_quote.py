import scrapy


class LoginQuoteSpider(scrapy.Spider):
    name = 'login-quote'
    allowed_domains = ['toscrape.com']
    login_url = 'http://quotes.toscrape.com/login'
    start_urls = [login_url]

    def parse(self, response):
        csrf_token = response.css('input[name="csrf_token"]::attr(value)').extract_first()
        data_login = {
            'csrf_token': csrf_token,
            'username': 'abc',
            'password': 'abc',
        }
        yield scrapy.FormRequest(url=self.login_url, formdata=data_login, callback=self.parse_quotes)

    def parse_quotes(self, response):
        quotes = response.css('div.quote')
        for quote in quotes:
            yield {
                'author_name': quote.css('small.author::text').extract_first(),
                'author_url': quote.css('small.author ~ a[href*="goodreads.com"]::attr(href)').extract_first(),
            }
