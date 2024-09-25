import time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC

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

# 1. 네이버 검색 페이지로 이동
def get_blog_search_results(query):
    url = f"https://search.naver.com/search.naver?ssc=tab.blog.all&sm=tab_jum&query={query}"

    driver = chrome_driver()
    driver.get(url)
    
    # 페이지 로딩 대기
    time.sleep(2)

    # 검색 결과 페이지 파싱
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    blog_posts = []
    for post in soup.select('.sh_blog_top'):  # 네이버 블로그 검색 결과의 CSS 셀렉터
        title_element = post.select_one('.sh_blog_title')  # 수정된 부분
        title = title_element.text.strip()
        link = title_element['href']
        date_posted = post.select_one('.txt_inline').text.strip()

        # 2. 12시간 이내의 글 필터링
        if '시간' in date_posted and int(date_posted.replace('시간 전', '').strip()) <= 12:
            blog_posts.append({'title': title, 'link': link, 'date_posted': date_posted})

    driver.quit()
    return blog_posts

# 3. 블로그 글 본문 스크래핑
def scrape_blog_content(blog_link):
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')
    driver.get(blog_link)

    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # 블로그 본문 추출
    content = soup.select_one('.se-main-container').text.strip()

    # 좋아요 갯수 및 댓글 수 추출
    likes = soup.select_one('.u_cnt._count').text if soup.select_one('.u_cnt._count') else '0'
    comments = soup.select_one('.u_cbox_count').text if soup.select_one('.u_cbox_count') else '0'

    # 댓글 내용 추출
    comment_elements = soup.select('.u_cbox_text_wrap')
    comments_text = [comment.text.strip() for comment in comment_elements]

    driver.quit()

    return {
        'content': content,
        'likes': likes,
        'comments_count': comments,
        'comments': comments_text
    }

# 전체 프로세스 실행
if __name__ == '__main__':
    search_query = '롯데카드'  # 원하는 검색어를 넣으세요
    blog_posts = get_blog_search_results(search_query)

    for post in blog_posts:
        print(f"제목: {post['title']}")
        print(f"링크: {post['link']}")
        print(f"게시 시간: {post['date_posted']}")
        
        blog_data = scrape_blog_content(post['link'])
        print(f"본문: {blog_data['content'][:200]}...")  # 본문 일부만 출력
        print(f"좋아요: {blog_data['likes']}, 댓글 수: {blog_data['comments_count']}")
        print(f"댓글: {blog_data['comments']}")
        print('-' * 50)
