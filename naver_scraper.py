import time
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def chrome_driver():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화
    chrome_options.add_argument('--disable-dev-shm-usage')  # /dev/shm 사용 비활성화
    chrome_options.add_argument('--remote-debugging-port=9222')  # 원격 디버깅 포트 설정
    chrome_options.add_argument('--headless')  # GUI 없이 실행 (헤드리스 모드)
    chrome_options.add_argument('--disable-gpu')  # GPU 비활성화 (일부 환경에서 필요)
    chrome_options.add_argument('--disable-software-rasterizer')  # 소프트웨어 래스터라이저 비활성화
    service = Service("C:\chromedriver\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

def scroll_to_bottom(driver):
    """페이지 끝까지 스크롤하는 함수"""
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # 새로운 콘텐츠가 로드될 때까지 대기

        # 새로운 스크롤 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")

        # 더 이상 새로운 콘텐츠가 없으면 스크롤 중단
        if new_height == last_height:
            break
        last_height = new_height

user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}

base_url = "https://search.naver.com/search.naver"
keyword = input("검색 키워드 입력:")
page = 1

blog_params = {
            'ssc': 'tab.blog.all',
            'query': keyword,
            'sm': 'tab_jum',
            'sort': '0',
            'start': page
        }

cafe_params = {
            'ssc': 'tab.cafe.all',
            'query': keyword,
            'sm': 'tab_jum',
            'sort': '0',
            'start': page
        }

try:
    response = requests.get(base_url, params=blog_params, headers=headers)
    response.raise_for_status()
except requests.exceptions.HTTPError as http_err:
    print(f"HTTP 에러 발생: {http_err}")
except requests.exceptions.RequestException as req_err:
    print(f"요청 에러 발생: {req_err}")
except Exception as err:
    print(f"다른 에러 발생: {err}")

soup = BeautifulSoup(response.content, 'html.parser')

for post in soup.select('div.view_wrap'):
    title_tag = post.select_one('a.title_link')
    time_tag = post.select_one('span.sub')
    
    if title_tag:
        title = title_tag.get_text()
        href = title_tag['href']

    post_time = time_tag.get_text() if time_tag else "작성 시간 없음"
    print(title, post_time, href)


today = datetime.now().date()
time_lapse = today - timedelta(hours=12)