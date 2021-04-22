# 주요 라이브러리 활용
## requests 모듈 사용
### 1. 웹 페이지 추출
-  `urllib`보다 `requests`를 사용하면 쉽게 웹페이지 내용 추출 가능.
- `requests`는 HTTP 헤더, Basic 인증 등에 처리를 쉽고 제공.
- 문자 코드 변환, 압축 등을 자동으로 처리.
#### 예제코드
```python
r = requests.get(url)  # url에 해당하는 웹페이지 가져오기, r은 response 객체  
r.headers  # header값 가져오기  
r.text  # 본문 가져오기
r.content  # 본문 bytes 자료형으로 가져오기
```
---
### 2. Response 객체  
- `response` 객체의 `text`속성을 기반으로 유니코드 문자열을 쉽게 추출 가능.
- HTTP 헤더에서 응답 본문의 인코딩 방식을 추출 => `r.headers['Content-Type]`
- `response` 객체에는 `json()` 메서드가 있어 JSON 형식의 응답을 간단하게 디코드하여 `dict` 또는 `list`로 반환.
- `requests`에는 `post()`, `put()`, `delete()`, `head()`, `options()` 메서드 존재.
#### 예제코드
```python
r = requests.post(url, data={'key1': 'value1'})  # post 형식으로 body에 데이터를 넣고 요청
r = requests.get(url, headers={'key1': 'value1'})  # get 형식으로 header에 데이터를 넣고 요청
r = requests.get(url, params={'key1':'value1'})  # get 형식으로 parameter를 넣고 요청
```
---
### 3. Session 다루기
- 여러 개의 페이지를 연속으로 크롤링할 때는 `Session` 객체를 사용하여 HTTP 헤더, Basic 인증을 한번만 하여 여러번 재사용 가능.
- `Session` 객체를 사용해 같은 웹사이트에 여러 번 요청할 때는 HTTP Keep-Alive 접속 방식 사용. 이 방법은 서버측 부하를 줄일 수 있음.
#### 예제코드
```Python
s = requests.Session()  # session객체 생성
s.headers.update({'key': 'value'})  # session 객체의 header에 데이터 넣기
r = s.get(url)  # 해당 url로 session객체를 통한 get 요청
```
---
## Beautiful Soup를 이용한 스크레이핑
### Beautiful Soup에서 사용할 수 있는 파서  
|파서|매개변수에 지정하는 문자열|특징|
|:---:|:---:|:---:|
|표준라이브러리html.parser|`html.parser`|추가 라이브러리가 필요하지 않음.|
|lxml의 HTML 파서|`lxml`|빠른 처리가 가능.|
|lxml의 XML 파서|`lxml-xml` or `xml`|XML에 대해 빠른 처리가 가능.|
|html5lib|`html5lib`|html5lib를 사용해 HTML5의 사양에 맞게 파싱 가능.|
#### 예제코드
```python
with open(*.html) as f:
    soup = BeautifulSoup(f, 'html.parser')  # html.parser로 html 파일 열기
soup.tagname  # <h1>, <div> 등 해당 태그 출력
soup.tagname.text  # 해당 태그에 속한 내용을 string으로 가져오기
soup.tagname['key']  # 해당 태그 객체를 딕셔너리처럼 속성 추출 가능
soup.find(tagname, class_=classname)  # 해당 태그의 첫번째 요소 추출, 해당 classname 요소 추출
soup.find_all(tagname, class_=classname)  # 해당 태그의 모든 요소 추출, 해당 classname 요소 추출
soup.select(cssname)  # 해당 css name의 요소 추출
soup.tagname.attrs  # 해당 태그의 속성들을 모두 추출
soup.tagname.get(attrsname)  # 해당 태그의 속성에 대한 값 추출
```
---
>#### 실습코드
>```python
>import requests
>from bs4 import BeautifulSoup
>
>
>r = requests.get('https://www.hanbit.co.kr/store/books/new_book_list.html')
>charset = r.encoding
>decode = r.content.decode(charset)
>soup = BeautifulSoup(decode, 'html.parser')
>book_list = []
>for i in soup.find_all('li', class_='sub_book_list'):
>    title = i.find('p', class_='book_tit').text
>    price = i.find('span', class_='price').text
>    writer = i.find('p', class_='book_writer').text
>    url = 'http://www.hanbit.co.kr' + i.find('a').get('href')
>    code_idx = url.find('code=')
>    code = url[code_idx+5:]
>    book = {'title': title, 'price': price, 'writer': writer, 'url': url, 'code': code}
>    book_list.append(book)
>for i in range(len(book_list)):
>    print(book_list[i])
>    print('\n')
>```
