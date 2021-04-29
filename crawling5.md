## Scrapy
- 크롤링/스크레이핑을 위한 파이썬 프레임워크
- 풍부한 기능이 제공되어 사용자는 페이지에서 데이터를 추출하는 본질적인 작업에만 충실할 수 있음.
- 웹사이트 다운로드 처리를 비동기적으로 실행하므로 다운로드 중에도 스크레이핑 처리를 할 수 있음.
> 1. 웹페이지에서 링크 추출하기
> 2. robots.txt를 기반으로 허가된 페이지와 금지된 페이지 구분하기
> 3. XML 사이트맵 추출과 링크 추출하기
> 4. 도메인과 IP 주소마다 크롤링 시간 간격 조정하기
> 5. 여러 개의 크롤링 대상을 병렬 처리하기
> 6. 중복된 URL 크롤링하지 않기
> 7. 오류가 발생했을 때 특정 횟수만큼 재시도하기
> 8. 크롤러를 데몬으로 만들기와 잡 관리하기

## Spider
- `Scrapy`를 사용하면 주로 `Spider`라는 이름의 클래스를 만듬.
- 대상 웹사이트마다 `Spider`를 만들며, 이러한 `Spider`클래스에 크롤링 처리와 스크레이핑 처리를 작성함.
```python
import scrapy


# scrapy runspider myspider.py -o items.jl
# 스크레이핑 결과가 items.jl에 json line 형식으로 저장됨
class BlogSpider(scrapy.Spider):
    # 스파이더 이름
    name = 'blogspider'
    # 크롤링을 시작할 URL 리스트
    start_urls = ['https://blog.scrapinghub.com']

    def parse(self, response):
        # 최상위 페이지에서 카테고리 페이지의 링크를 추출
        for url in response.css('ul li a::attr("href")').re('.*/tag/.*'):
            yield scrapy.Request(response.urljoin(url), self.parse_titles)

    def parse_titles(self, response):
        # 카테고리 페이지에서 카테고리 타이틀을 모두 추출
        for post_title in response.css('div.post-header > h2 > a::text').extract():
            yield {'title': post_title}
```

## Scrapy Project로 관리하기
- `Scrapy`를 프로젝트라는 단위로 여러 개의 `Spider` 관련 클래스를 통합 관리할 수 있음.
- 일회용 `Spider`를 만드는 것이 아니라면 프로젝트를 사용하는 것이 기본.
- `scrapy startproject myproject-name` -> 프로젝트 생성.

## 뉴스 페이지 예제
### 1. Item 만들기 
- Items은 `Spider`가 추출할 데이터를 저장할 객체.
- 여러 종류의 데이터를 추출했을 때 클래스를 기반으로 객체를 판별 가능.
- 미리 정의한 필드에 데이터를 입력하므로, 필드 이름을 잘못 적는 실수를 줄일 수 있음.
- 메서드를 정의할 수 있음.
```python
## myproject/items.py ##
import scrapy


class Headline(scrapy.Item):
    # 뉴스 헤드라인을 나타내는 Item 객체
    title = scrapy.Field()
    body = scrapy.Field()

item = Headline()
item['title'] = 'Example'
print(item['title'])  # Example이 출력됨. dict 형식으로 데이터를 가져올 수 있음.
```

### 2. spider 만들기
- `scrapy genspider spider-name domain` 을 이용하여 템플릿을 기반으로 한 spider-name.py가 생성됨.
- `name` 속성에는 `Spider`의 이름을 설정.
- `allowed_domains` 속성에는 크롤링 대상 도메인 리스트를 지정. 링크를 이동하다 보면 예상하지 못한 웹페이지에 접근하는 경우를 막기 위해 사용.
- `start_urls` 속성에는 크롤링을 시작할 URL 목록을 리스트 또는 튜플 형식으로 지정. 여러개의 URL 지정 가능
- `parse()` 메서드는 추출한 웹 페이지 처리를 위한 콜백 함수.
- `Scrapy Shell`을 이용하면 `css` or `xpath`를 사용하는데 편리하게 테스트 형식으로 추출해볼 수 있음. (`scrapy shell url`)

* 주요 메서드
  
    | 메서드 | 기능 |
    |:---:|:---:|
    | `extract()` | 노드 목록을 문자열 list로 추출(태그 제거) |
    | `extract_first()` | 노드 목록의 첫 번째 요소를 문자열로 추출 |
    | `re(regex)` | 노드 목록에서 정규 표현식에 해당 노드만 문자열 list 추출 |
    | `re_first(regex)` | 노드 목록에서 정규 표현식에 해당하는 노드중 첫번째 문자열 list로 추출 |
    | `css(query)` | 노드 목록 요소에 대해 매개변수로 지정한 CSS 선택자에 해당하는 목록 SelectorList로 추출 |
    | `xpath(query)` | 노드 목록 요소에 대해 매개변수로 지정한 XPath에 해당하는 목록 SelectorList로 추출 |


```python
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
        # html > head > title에서 text만을 추출하고 태그를 제거한 첫번째 요소 반환
        item['title'] = response.css('html head title::text').extract_first()
        # div 태그에서 class가 article-text인 태그 내부에 p 태그에서 모든 string요소들을 가져와서 태그를 제거한 요소를 반환
        item['body'] = "".join(response.css('div.article-text p').xpath('string()').extract())
        yield item
```

### 3. 실행 흐름
1. Scrapy Engine
    - 다른 컴포넌트를 제어하는 실행 엔진
2. Scheduler
    - Request를 큐에 저장
3. Downloader
    - Request가 나타내는 URL의 페이지를 실제로 다운로드
4. Spider
    - 다운로드한 Response를 받고, 페이지에서 Item 또는 다음 순회 링크를 나타내는 Request를 추출
5. Feed Exporter
    - Spider가 추출한 Item을 파일 등에 저장
6. Item Pipline
    - Spider가 추출한 Item과 관련된 처리
7. Download Middleware
    - Downloader 처리를 확장
8. Spider Middleware
    - Spider에 입력되는 Response와 Spider에서 출력되는 Item/Request 대해 처리를 확장   
    
![](D:\CrawlingStudy\img\scrapy_archiecture.png)

> ### lxml, Beautiful Soup, Scrapy의 차이점
> - CSS 선택자로 title 요소의 텍스트 추출하기   
>   `html.cssselect('title').text` -> `lxml`   
>   `soup.select('title).text` -> `Beautiful Soup`   
>   `response.css('title::text').extract_first()` -> `Scrapy`
> - class='test'의 a 요소가 가진 href 속성 추출   
>   `html.cssselect('a.test').get('href)` -> `lxml`  
>   `soup.select('a.test')['href']` -> `Beautiful Soup`
>   `response.css('a.test::attr("href")').extract_first()` -> `Scrapy`

