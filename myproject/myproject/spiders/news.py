import scrapy
from myproject.items import Headline


class NewsSpider(scrapy.Spider):
    name = 'news'
    allowed_domains = ['engadget.com']
    start_urls = ['http://engadget.com/']

    def parse(self, response):
        # 메인 페이지의 토픽 목록에서 기사 링크를 추출하고 출력
        link = response.css('article div a::attr("href")').extract()
        # 기사만 추출하기 위한 필터링
        link = list(filter(lambda x: x[-4:] == 'html' and x[0] == '/', link))
        for url in link:
            yield scrapy.Request(response.urljoin(url), self.parse_topics)

    def parse_topics(self, response):
        item = Headline()
        item['title'] = response.css('html head title::text').extract_first()
        item['body'] = "".join(response.css('div.article-text p').xpath('string()').extract())
        yield item

