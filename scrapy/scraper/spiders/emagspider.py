import time
import scrapy

from scraper.items import ScraperItem


class EmagspiderSpider(scrapy.Spider):
    name = "emagspider"
    allowed_domains = ["emag.ro"]
    start_urls = ["https://www.emag.ro/search/ryzen%209?ref=effective_search"]

    def parse(self, response):
        items = response.css('div.card-item')
        for item in items:
            item_url = item.css('h2 a.card-v2-title').attrib.get('href', 'Not available')
            if item_url is 'Not available': continue
            yield response.follow(item_url, self.parse_item_page)
            break
        return
        next_page = response.css('a.js-change-page::attr(href)').get()
        if next_page is not None:
            next_page = 'https://www.emag.ro' + next_page
            yield response.follow(next_page, self.parse)
        
    def parse_item_page(self, response):
        time.sleep(2)
        table_rows = response.css("table.specifications-table tr")
        scraper_item = ScraperItem()
        scraper_item['name'] = response.css('h1.page-title::text').get(),
        scraper_item['url'] = response.url,
        scraper_item['price'] = response.css('p.product-new-price::text').get(),
        scraper_item['specs'] = {row.css("td ::text").get(): row.css("td:nth-child(2) ::text").get() for row in table_rows},
        scraper_item['availability'] = response.css("span.label-out_of_stock::text").get() != "Stoc epuizat",
        scraper_item['num_reviews'] = response.css("a.rating-text span::text").get(),
        scraper_item['rating'] = response.css("a.rating-text::text").get(),
        scraper_item['category'] = response.xpath("//ol[@class='breadcrumb']/li[@class='active']/preceding-sibling::li[1]/a/text()").get(),
        scraper_item['img_url'] = response.css("a.product-gallery-image::attr(href)").get(),
        print(" =========================================== Scraped item:")
        print(scraper_item)
        yield scraper_item
        