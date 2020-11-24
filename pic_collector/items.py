# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PicCollectorItem(scrapy.Item):
    # define the fields for your item here like:
    description = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
