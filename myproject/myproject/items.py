# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Headline(scrapy.Item):
    # 뉴스 헤드라인을 나타내는 Item 객체
    title = scrapy.Field()
    body = scrapy.Field()


class Restaurant(scrapy.Item):
    name = scrapy.Field()
    address = scrapy.Field()
    phone = scrapy.Field()
    traffic = scrapy.Field()

