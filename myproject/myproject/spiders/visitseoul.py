import scrapy
from myproject.items import Restaurant
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import re


class VisitseoulSpider(CrawlSpider):
    name = 'visitseoul'
    allowed_domains = ['korean.visitseoul.net']
    start_urls = ['http://korean.visitseoul.net/restaurants?curPage=1']

    rules = [
        # 음식점 모든 페이지 순회
        Rule(LinkExtractor(allow=r'/restaurants\?curPage=\d$')),
        # 음식점 상세 페이지 분석
        Rule(LinkExtractor(allow=r'/restaurants/\w+/\d+'),
             callback='parse_restaurant')
    ]

    def parse_restaurant(self, response):
        name = response.css('h3').xpath('string()').extract_first()
        address = response.css('dl:contains("주소") dd').xpath('string()').extract_first()
        phone = response.css('dl:contains("전화번호") dd').xpath('string()').extract_first()
        traffic = response.css('dl:contains("교통 정보") dd').xpath('string()').extract_first()

        item = Restaurant(
            name=name,
            address=address,
            phone=phone,
            traffic=traffic
        )
        yield item
