import time
import datetime
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

user_agent = UserAgent()
headers = {'User-Agent': user_agent.random}

base_url = "https://search.naver.com/search.naver"
# https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query=%EB%A1%AF%EB%8D%B0%EC%B9%B4%EB%93%9C
# https://search.naver.com/search.naver?ssc=tab.cafe.all&sm=tab_jum&query=%EB%A1%AF%EB%8D%B0%EC%B9%B4%EB%93%9C
# https://search.naver.com/search.naver?ssc=tab.news.all&where=news&sm=tab_jum&query=%EB%A1%AF%EB%8D%B0%EC%B9%B4%EB%93%9C
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
            'ssc': 'tab.blog.all',
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
post = soup.select('a.title_link')
print(post)

today = datetime.now().date()
    
print(f"오늘은 {today} 입니다.")
three_days_ago = today - timedelta(days=3)

blog_posts = []
for post in soup.select('.sh_blog_top'):  # 네이버 블로그 검색 결과의 CSS 셀렉터
    title = post.select_one('a.title_link').text.strip()
    link = post.select_one('.sh_blog_title')['href']
    date_posted = post.select_one('.txt_inline').text.strip()

    # 2. 12시간 이내의 글 필터링
    if '시간' in date_posted and int(date_posted.replace('시간 전', '').strip()) <= 12:
        blog_posts.append({'title': title, 'link': link, 'date_posted': date_posted})

print(blog_posts)