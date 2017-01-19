import scrapy


class CardSpider(scrapy.Spider):
    name = "card_spider"

    def start_requests(self):
        url_root = 'https://shadowverse-portal.com/cards?m=index&m=index&card_offset='
        current_card_count = 624
        cards_per_page = 12

        for i in range(0, current_card_count, cards_per_page):
            url = url_root + str(i)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.css('div.quote'):
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.css('span small::text').extract_first(),
            }

        next_page = response.css('li.next a::attr(href)').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

    def parse_card(self, card_obj):
        assert type(card_obj) == scrapy.selector.unified.SelectorList
        # follow link to card page
        # parse name
        # parse details
        # parse attrs

    def parse_card_name(self, response):
        return response.css('h1.card-main-title::text').extract_first().strip()

    def parse_details(self, response):
        ul = response.css('ul.card-info-content')
        lis = ul.css('li')
        # implement later. Liquefy and Card Pack don't use spans for their content
        pass

    def parse_attrs(self, response):
        lis = response.css('ul.card-main-list').css('li')
        if len(lis) == 1:
            return parse_card_text()
        elif len(lis) == 2:
            return parse_creature()

    def parse_card_text(self, selector):
        print(type(selector))
        assert type(selector) == scrapy.http.response.html.HtmlResponse
        return {
            'text': selector.css('p.card-content-skill::text').extract_first().strip()
        }

