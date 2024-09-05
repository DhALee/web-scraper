import os
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.sitemap import SitemapLoader
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

os.environ['USER_AGENT'] = random.choice(user_agents)
print(os.environ['USER_AGENT'])

def html_links():
    url = 'https://www.lottecard.co.kr/app/LPBNFDA_V100.lc'  # 원하는 URL로 변경하세요
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    print(links)

def check_links_change(driver, initial_links_count):
    current_links_count = len(driver.find_elements(By.TAG_NAME, 'a'))
    print(f"현재 링크 개수: {current_links_count}")
    return current_links_count != initial_links_count

def hc_event(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화
    chrome_options.add_argument('--disable-dev-shm-usage')  # /dev/shm 사용 비활성화
    chrome_options.add_argument('--remote-debugging-port=9222')  # 원격 디버깅 포트 설정
    chrome_options.add_argument('--headless')  # GUI 없이 실행 (헤드리스 모드)
    chrome_options.add_argument('--disable-gpu')  # GPU 비활성화 (일부 환경에서 필요)
    chrome_options.add_argument('--disable-software-rasterizer')  # 소프트웨어 래스터라이저 비활성화
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    url = url  # 원하는 URL로 변경하세요
    driver.get(url)

    # 자바스크립트가 실행되도록 잠시 대기
    time.sleep(5)  # 필요 시 적절한 시간으로 조정 가능

    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')

    while True:
        initial_links_count = len(driver.find_elements(By.TAG_NAME, 'a'))
        try:

            links = []
            for link in soup.find_all('a', href=True):
                links.append(link['href'])
            
            if 'javascript:pageing();' in links:
                # print(links)
                print("페이지 로드 중입니다.")
                driver.execute_script("pageing();")
                WebDriverWait(driver, 5).until(lambda driver: check_links_change(driver, initial_links_count))

                page_source = driver.page_source
                soup = BeautifulSoup(page_source, 'html.parser')
                
            else:
                print("더 이상 로드할 페이지가 없습니다.")
                break  # 더 이상 새로운 데이터가 없으면 반복 종료

        except Exception as e:
            print("에러 발생 또는 더 이상 페이지가 없습니다.", e)
            break
    
    links = []
    for link in soup.find_all('a', href=True):
            links.append(link['href'])

    # print(f"전체 링크: {links}")
    # final_links_count = len(driver.find_elements(By.TAG_NAME, 'a'))
    # print(f"최종 링크 개수: {final_links_count}")
    
    filtered_links = [element for element in links if '/cpb/ev/CPBEV0101_06.hc' and '&searchWord=' in element]
    # print(filtered_links)

    hc = "https://www.hyundaicard.com" 
    event_links = []
    for filtered_link in filtered_links:
        event_links.append(hc + filtered_link)
    print(event_links)

    driver.quit()

    return event_links

def site():

    loader = SitemapLoader(
        web_path="https://api.python.langchain.com/sitemap.xml"
    )
    data = loader.load()
    print(data)

def web(link):
    loader = WebBaseLoader(
        web_path=f"{link}"
    )
    documents = loader.load()
    print(documents)

if __name__ == "__main__":
    url = 'https://www.hyundaicard.com/cpb/ev/CPBEV0101_01.hc'
    event_links = hc_event(url)
    for event_link in event_links:
        web(event_link)