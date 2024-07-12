import requests
from bs4 import BeautifulSoup
import schedule
import time, sys
from langchain_community.llms import Ollama
from langchain_core.prompts import PromptTemplate

def reputation(text):

    title_content = Ollama(model="llama3:70b")
    string_prompt = (
        PromptTemplate.from_template(("""I want you to take the HTML {text} of the news webpage and extract just the title and body of a news article. 
                I will provide you with the {text} in HTML format, and you will separate the title and body of the article from that text and organize it neatly.

                All answers must be in Korean.
                                    """))
    )

    string_prompt_value = string_prompt.format_prompt(text=text)
    news_neat = title_content.invoke(string_prompt_value)

    print("-"*100)
    print(news_neat)
    print("-"*100)

    reputation_analysis = Ollama(model="llama3:70b")
    string_prompt = (
        PromptTemplate.from_template(("""I want you to act as a reputation management system to collect and manage LOTTE Card's reputation through the news or the internet {text}. 
                                        I will provide you with a specific news article or online review {text}, and you will analyze the content, 
                                        classify whether LOTTE Card's reputation is positive, negative, or neutral, and summarize the main points. 
                                        In the case of a negative reputation, you will also include suggestions for improvement.
                                        If the text provided is not relevant to LOTTE Card, please write Null.

                                        All answers must be in Korean.
                                    """))
    )

    string_prompt_value = string_prompt.format_prompt(text=news_neat)
    result = reputation_analysis.invoke(string_prompt_value)

    print("-"*100)
    print(result)
    print("-"*100)

    return result

def extract_naver_news(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.prettify()

    title_tag = soup.find('h2', {'class': 'media_end_head_headline'})
    if not title_tag:
        title_tag = soup.find('h3', {'class': 'tts_head'})
    title = title_tag.get_text(strip=True) if title_tag else "제목을 찾을 수 없습니다."
    
    content_tag = soup.find('div', {'id': 'dic_area'})
    if not content_tag:
        content_tag = soup.find('div', {'class': 'article_body'})
    content = ' '.join([p.get_text(strip=True) for p in content_tag.find_all('p')]) if content_tag else "본문을 찾을 수 없습니다."
    
    return news, title, content

def search_naver_news(keyword):
    base_url = "https://search.naver.com/search.naver"
    params = {
        'where': 'news',
        'query': keyword,
        'sm': 'tab_pge',
        'sort': '0',  # 최신순 정렬
        'start': 1  # 첫 번째 페이지
    }

    response = requests.get(base_url, params=params)
    print(response)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    article_urls = []
    # for link in soup.select('.news .news_wrap a'):
    #     article_urls.append(link['href'])

    for link in soup.select('.news_tit'):
        # print(link)
        article_urls.append(link['href'])
    
    print("Number of articles: ", len(article_urls))
    return article_urls

def monitor_naver_news(keyword):
    article_urls = search_naver_news(keyword)
    for url in article_urls:
        print(url)
        news, title, content = extract_naver_news(url)
        rep = reputation(news)
        # print(title)
        # print(content)
        # if keyword in title or keyword in content:
        #     print(f'키워드 "{keyword}"가 포함된 기사 발견!')
        #     print(f'기사 제목: {title}')
        #     print(f'기사 본문: {content}')
        #     print(f'기사 URL: {url}')
        # else:
        #     print(f'키워드 "{keyword}"가 포함된 기사가 없습니다.')

def main():
    keyword = input("모니터링할 키워드를 입력하세요: ")
    # monitor_naver_news(keyword)
    # 주기적으로 모니터링 작업 수행 (예: 5분마다)
    schedule.every(5).minutes.do(monitor_naver_news, keyword=keyword)
    
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()