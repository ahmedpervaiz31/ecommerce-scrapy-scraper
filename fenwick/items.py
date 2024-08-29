# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class FenwickClothesItem(scrapy.Item):
    brand = scrapy.Field()
    name = scrapy.Field()
    images_url = scrapy.Field()
    price = scrapy.Field()