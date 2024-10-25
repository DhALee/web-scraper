import os
import re
import time
import random
from bs4 import BeautifulSoup
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

def bs_event(url):
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-software-rasterizer')
    service = Service('/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=chrome_options)

    driver.get(url)

    time.sleep(3)

    elements = driver.find_elements(By.CSS_SELECTOR, '.ml-20')

    for idx in range(len(elements)):
        try:
            current_url = driver.current_url
            elements = driver.find_elements(By.CSS_SELECTOR, '.ml-20')
            element = elements[idx]
            element.click()
            
            WebDriverWait(driver, 5).until(EC.url_changes(current_url))
            
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            page_text = soup.get_text(separator='\n', strip=True)
            
            if page_text.strip():
                with open(f'/svc/project/genaipilot/web-scraper/bs_files/{idx}.txt', 'w', encoding='utf-8') as file:
                    pattern = re.compile(r"이벤트 대상 카드로\n(.*?심의필)", re.DOTALL)
                    matches = pattern.findall(page_text)

                    if matches:
                        print(f"{driver.current_url} {idx}.txt 저장 중")
                        for match in matches:
                            file.write(match)
                    else:
                        print("No match found.")
                        file.write("No match found.")
            else:
                print(f"{idx}.txt 저장되지 않음: 텍스트가 비어 있음")
            
            driver.back()
        except Exception as e:
            print(f"Failed to process element {idx}: {e}")
            continue
        
    driver.quit()

if __name__ == "__main__":
    url = 'https://www.banksalad.com/chart/cards?tab=event'
    bs_event(url)
