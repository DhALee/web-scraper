import os
import re
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.document_loaders.sitemap import SitemapLoader
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
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
                WebDriverWait(driver, 3).until(lambda driver: check_links_change(driver, initial_links_count))

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
    # print(event_links)
    
    for event_link in event_links:
        driver.get(event_link)
        print(event_link)
        name = event_link.split('=')[1].split('&')[0]
        time.sleep(3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        page_text = soup.get_text()

        # with open(f'/svc/project/genaipilot/web-scraper/html_files/{name}.html', 'w', encoding='utf-8') as file:
        #     print(f"{name}.html 저장 중")
        #     file.write(page_source)

        with open(f'/svc/project/genaipilot/web-scraper/test_files/{name}.txt', 'w', encoding='utf-8') as file:
            print(f"{name}.txt 저장 중")

            pattern = re.compile(r"(이벤트\n\n\n\n.*?심의필)", re.DOTALL)
            matches = pattern.findall(page_text)
            if matches:
                for match in matches:
                    print(match)
                    file.write(match)
            else:
                print("No match found.")

            # pattern = re.compile(r"이벤트\n\n\n\n(.*?)심의필", re.DOTALL)
            # match = pattern.search(page_text)
            # if match:
            #     result = match.group(1).strip()
            #     print(result)
            #     file.write(result)
            # else:
            #     print("No match found.")

    driver.quit()

def read_text(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')  # 샌드박스 비활성화
    chrome_options.add_argument('--disable-dev-shm-usage')  # /dev/shm 사용 비활성화
    chrome_options.add_argument('--remote-debugging-port=9222')  # 원격 디버깅 포트 설정
    chrome_options.add_argument('--headless')  # GUI 없이 실행 (헤드리스 모드)
    chrome_options.add_argument('--disable-gpu')  # GPU 비활성화 (일부 환경에서 필요)
    chrome_options.add_argument('--disable-software-rasterizer')  # 소프트웨어 래스터라이저 비활성화
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    # 웹페이지 열기
    url = url
    driver.get(url)

    # 페이지 HTML 소스 가져오기
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    page_text = soup.get_text()

    with open(f'/svc/project/genaipilot/web-scraper/test.txt', 'w', encoding='utf-8') as file:
        file.write(page_text)

    # 브라우저 닫기
    driver.quit()

def cg_event(url):
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
    
    modals = driver.find_elements(By.CSS_SELECTOR, '.ctnr a')

    for idx, modal in enumerate(modals):
        try:
            modal.click()
            WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.ID, 'modal')))
            modal_content = driver.find_element(By.ID, 'modal').text
            # print(modal_content)

            if modal_content.strip():
                with open(f'/svc/project/genaipilot/web-scraper/cg_files/modal_{idx}.txt', 'w', encoding='utf-8') as file:
                    print(f"modal_{idx}.txt 저장 중")
                    file.write(modal_content)

            webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
            WebDriverWait(driver, 5).until(EC.invisibility_of_element_located((By.ID, 'modal')))
        
        except Exception as e:
            # print(f"Failed to process popup {idx}: {e}")
            continue

    links = []
    for link in soup.find_all('a', href=True):
        links.append(link['href'])

    filtered_links = [element for element in links if '/card/detail/' in element]
    card_links = list(set(filtered_links))
    # print(card_links)
    # print(len(card_links))
    cg = 'https://www.card-gorilla.com'
    event_links = []
    for card_link in card_links:
        event_links.append(cg + card_link)

    for event_link in event_links:
        driver.get(event_link)
        print(event_link)
        name = event_link.split('/')[-1]
        time.sleep(3)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        page_text = soup.get_text()

        with open(f'/svc/project/genaipilot/web-scraper/cg_files/{name}.txt', 'w', encoding='utf-8') as file:
            print(f"{name}.txt 저장 중")
            file.write(page_text)

    driver.quit()


if __name__ == "__main__":
    # url = 'https://www.hyundaicard.com/cpb/ev/CPBEV0101_01.hc'
    url = 'https://www.card-gorilla.com/event'
    # hc_event(url)
    cg_event(url)

