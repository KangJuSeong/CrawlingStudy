## Selenium
### 자바스크립트를 이용한 페이지 스크래핑
- 웹사이트에 접근 했을 때 `HTML`과 `JavaScript` 등의 필요한 리소스를 로드 후 이후에 작업은 모두 `JavaScript`로 운용됨.
- 이런 구조를 `SPA`라고 하며, `SPA`구조의 페이지에서는 `HTML`만으로는 원하는 데이터가 표시되어 있지 않을 수 있음.
- 이럴 때 `Selenium`을 이용하여 원격으로 페이지 내에서 데이터를 가져올 수 있도록 해야 함.

### Selenium 사용 방법
- `send_keys()` 메서드를 이용하여 키보드 입력을 하고 어떤 버튼을 누르는 행위가 가능.
- `save_screenshot()` 메서드를 이용하여 스크린샷을 찍을 수 있음.
- `Chrome`, `Firefox`, `PhantomJS` 등을 사용할 수 있음.
- `find_elements_by_css_selector()` 메서드를 이용하여 css 태그의 요소들을 가져올 수 있음.
- `get_attribute()` 메서드를 이용하여 속성을 추출할 수 있음.
- 요소 내부에서 요소를 추가로 탐색 가능

### Selenium을 이용한 구글 검색
```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

# 크롬 드라이버를 이용
driver = webdriver.Chrome()
driver.get('https://www.google.co.kr')  # 구글 주소로 연결

assert 'Google' in driver.title  # 구글에 맞게 들어왔는지 확인

input_element = driver.find_element_by_name('q')  # q 라는 input 요소를 찾기(검색창)
input_element.send_keys('Python')  # python을 검색창에 입력
input_element.send_keys(Keys.RETURN)  # 검색 버튼 누르기

assert 'Python' in driver.title  # Python으로 검색이 잘 되었는지 확인

driver.save_screenshot('search_results.png')  # 스크린샷 찍기
for a in driver.find_elements_by_css_selector('h3 > a'):  # css 태그를 이용하여 필요한 요소들 가져오기
    print(a.text)
    print(a.get_attribute('href'))
    print()
driver.set_window_size(800, 600)  # 반응형 웹 등의 동작을 확인할 경우 창의 사이즈 늘리기
```

### 네이버 페이 주문 이력 추출하기
```python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import sys
import time

# input()을 통해 네이버 아이디와 비밀번호 입력 받기
NAVER_ID = input()
NAVER_PASSWORD = input()

# 메인 함수
def main():
    driver = webdriver.Chrome()
    driver.set_window_size(800, 600)
    sign_in(driver)
    navigate(driver)
    goods = scrape_history(driver)
    print(goods)

# form 형태에 id와 pw를 입력 후 로그인 요청
def sign_in(driver):
    print('Navigation...', file=sys.stderr)
    print('Waiting for sign in page loaded...', file=sys.stderr)
    time.sleep(2)
    driver.get('https://nid.naver.com/nidlogin.login')
    e = driver.find_element_by_id('id')
    e.clear()
    e.send_keys(NAVER_ID)
    e = driver.find_element_by_id('pw')
    e.clear()
    e.send_keys(NAVER_PASSWORD)
    form = driver.find_element_by_css_selector("input.btn_global[type=submit]")
    form.submit()

# 네이버페이 주문내역 페이지로 이동 후 더보기 버튼을 클릭하여 과거 이력 조회
def navigate(driver):
    print('Navigating...', file=sys.stderr)
    driver.get('https://order.pay.naver.com/home?tabMenu=SHOPPING')
    
    print('Waiting for contents to be loaded...', file=sys.stderr)
    time.sleep(2)
    
    driver.execute_script('scroll(0, document.body.scrollHeight)')  # 스크롤 하기
    wait = WebDriverWait(driver, 10)
    driver.save_screenshot('note-1.png')
    
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_moreButton a')))
    button.click()
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#_moreButton a')))
    button.click()
    
    print('Waiting for contetns to be loaded...', file=sys.stderr)
    time.sleep(2)
    
# 조회된 이력에서 css 태그들을 통해 필요한 데이터 가져오기
def scrape_history(driver):
    goods = []
    for info in driver.find_element_by_css_selector('.p_info'):
        link_element = info.find_element_by_css_selector('a')
        title_element = info.find_element_by_css_selector('span')
        date_element = info.find_element_by_css_selector('.date')
        price_element = info.find_element_by_css_selector('em')
        goods.append({
            'url': link_element.get_attribute('.a'),
            'title': title_element.text,
            'description': date_element.text + "-" + price_element.text + "원"
        })
    return goods
    

if __name__ == '__main__':
    main()
```



