import scrapy


class EmagspiderSpider(scrapy.Spider):
    name = "emagspider"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/search/ryzen%209?ref=effective_search"]

    def parse(self, response):
        items = response.css('div.card-item')
        for item in items:
            yield {
                'name': item.css('h2 a.card-v2-title::text').get(),
                'price': item.css('p.product-new-price::text').get(),
                'url': item.css('h2 a.card-v2-title').attrib.get('href', 'Not available')
            }
        next_page = response.css('a.js-change-page::attr(href)').get()
        if next_page is not None:
            next_page = 'https://www.emag.ro' + next_page
            yield response.follow(next_page, self.parse)
