# OPEN API를 이용한 크롤링
### Twiter open API 사용하기
1. Restfull API
    - 일반적인 API로서 15분에 15회만 호출할 수 있는 제한이 존재.
2. Streaming API
    - 한번 요청을 통해 서버와의 Connection을 유지하고 새로운 데이터가 추가될 때마다 서버가 데이터를 전송.
    
#### Restfull API 사용하기
- `requests`에 `OAuth` 인증을 추가하는 `Requests-OAuthlib` 사용
```python
import os
from requests_oauthlib import OAuth1Session

# 개인 키값을 환경변수를 통하 저장
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']

# 사용자 인증정보를 가진 Session 객체 생성
twitter = OAuth1Session(CONSUMER_KEY,
                        client_secret=CONSUMER_SECRET,
                        resource_owner_key=ACCESS_TOKEN,
                        resource_owner_secret=ACCESS_TOKEN_SECRET)

# 사용자의 타임라인 추출
response = twitter.get('https://api.twitter.com/1.1/statuses/home_timeline.json')

# API 응답을 json 형태로 파싱 후 사용자 이름과 트윗을 출력
for status in response.json():
    print(status['user']['screen_name'], status['text'])
```

### 유튜브에서 동영상 정보 수집하기
```python
import os
from apiclient.discovery import build


YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
# build() 함수 첫번째 파라미터는 API 이름, 두번째는 버전, 세번째는 API key 값 입력
# 함수 내부에서 자체적으로 https://www.googleapis.com/discovery/v1/apis/youtube/v3/rest로 접근
youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
# search.list 메서드를 호출하면 httpRequest가 반환되고 execute()을 실행하면 실제 http요청이 보내지고 응답이 반환됨
search_response = youtube.search().list(
   part='snippet',
   q='요리',
   type='video'
).execute()
for item in search_response['item']:
   # 검색 결과에 해당하는 동영상의 제목 출력
    print(item['snippet']['title'])
```



