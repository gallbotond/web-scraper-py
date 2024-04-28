# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def serialize_name(value):
    return value.strip()

def serialize_price(value):
    return value.strip()

class ScraperItem(scrapy.Item):
    name = scrapy.Field()  
    url = scrapy.Field()
    price = scrapy.Field() 
    specs = scrapy.Field()
    availability = scrapy.Field()
    num_reviews = scrapy.Field()
    rating = scrapy.Field()
    category = scrapy.Field()
    img_url = scrapy.Field()
