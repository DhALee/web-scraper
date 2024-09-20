import requests
from bs4 import BeautifulSoup
import time, sys, os, re, random, html
from datetime import datetime, timedelta

user_agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.1 Safari/605.1.15',
    ]

headers = {'User-Agent':random.choice(user_agents)}
print(headers)

def extract_naver_news(url, press_name, article_date):
    time_stamp = int(time.time())
    current_path = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(current_path, f"news/naver_{time_stamp}.html")
    
    # os.environ['USER_AGENT'] = random.choice(user_agents)
    # print(os.environ['USER_AGENT'])
    

    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    # }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 에러 발생: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"요청 에러 발생: {req_err}")
    except Exception as err:
        print(f"다른 에러 발생: {err}")

    soup = BeautifulSoup(response.content, 'html.parser')
    news = soup.prettify()

    title_tag = soup.title
    title = title_tag.get_text(strip=True) if title_tag else None
    
    article_body_tag = soup.find('div', {'itemprop': 'articleBody'})
    if article_body_tag:
        # 본문 텍스트를 추출
        article_text = article_body_tag.get_text(strip=True)
        # print("기사 본문:\n", article_text)
    else:
        print("기사 본문을 찾을 수 없습니다.")
    
    # content_tag = soup.find('div', {'id': 'dic_area'})
    # if not content_tag:
    #     content_tag = soup.find('div', {'class': 'article_body'})
    # content = ' '.join([p.get_text(strip=True) for p in content_tag.find_all('p')]) if content_tag else "본문을 찾을 수 없습니다."

    if title is not None:
        unescaped_title = html.unescape(title)
        # print(unescaped_title)
        safe_title = re.sub(r'[\\/*:<>|?!\'"\.,]', "_", unescaped_title)
        clean_result = re.split(r' -|_', safe_title)

        if clean_result[0] == '':
            new_result = ''
            for x in clean_result:
                if x != '':
                    if x == ' ':
                        break
                    new_result += x
            html_path = os.path.join(current_path, f"news/{new_result}, {press_name}.html")
        else:
            html_path = os.path.join(current_path, f"news/{clean_result[0]}, {press_name}.html")
    else:
        html_path = os.path.join(current_path, f"news/{time_stamp}.html")

    print(html_path)
    try:
        with open(html_path, 'w', encoding='utf-8') as f:
            # f.write(news)
            if article_body_tag:
                f.write(f"{url}\n")
                f.write(f"{title}\n")
                f.write(f"{press_name}\n")
                f.write(f"{article_date}\n")
                f.write(article_text)
            else:
                f.write(news)
    except OSError as e:
        print(f"파일 경로 오류: {e}")
        # with open(html_path, 'w', encoding='utf-8') as f:
        #     f.write(news)

    return news, title, article_text

def convert_to_isoformat(date_string):
    date_string = date_string.strip()
    try:
        # 형식 1: 'YYYY.MM.DD HH:MM'
        if '.' in date_string and ' ' in date_string:
            date_object = datetime.strptime(date_string, '%Y.%m.%d %H:%M')
        # 형식 2: ISO 8601 형식 '2024-09-18T08:30:00+0900' 처리
        elif 'T' in date_string and ('+' in date_string or '-' in date_string):
            # 타임존 오프셋 수정: +0900 -> +09:00
            if date_string[-5] in ['+', '-']:
                date_string = date_string[:-5] + date_string[-5:-2] + ':' + date_string[-2:]
            date_object = datetime.fromisoformat(date_string)
        # 형식 3: 'YYYYMMDDTHHMMSS'
        elif len(date_string) == 15 and 'T' in date_string:
            date_object = datetime.strptime(date_string, '%Y%m%dT%H%M%S')
        # 형식 4: '2024-08-28T10:11:55Z' (UTC 타임존)
        elif date_string.endswith('Z'):
            date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        elif ' ' in date_string and '-' in date_string:
            date_object = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
        else:
            raise ValueError("지원되지 않는 날짜 형식")

        iso_format_string = date_object.isoformat()

        return iso_format_string
    except ValueError as e:
        print(f"날짜 변환 오류: {e}")

def search_naver_news(keyword, preferred_press=None):
    base_url = "https://search.naver.com/search.naver"
    start = 1

    today = datetime.now().date()
    
    print(f"오늘은 {today} 입니다.")

    # 날짜를 조정하고 싶으면 아래 코드를 수정하세요. e.g. days=2, days=1, days=0
    three_days_ago = today - timedelta(days=3)

    article_urls = []
    # 검색 페이지 범위를 조정하고 싶으면 range 코드를 수정하세요.
    for page in range(10):
        params = {
            'where': 'news',
            'query': keyword,
            'sm': 'tab_pge',
            'sort': '0',
            'start': start
        }

        try:
            response = requests.get(base_url, params=params, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP 에러 발생: {http_err}")
        except requests.exceptions.RequestException as req_err:
            print(f"요청 에러 발생: {req_err}")
        except Exception as err:
            print(f"다른 에러 발생: {err}")

        soup = BeautifulSoup(response.content, 'html.parser')

        start += 10
        time.sleep(2)


        for link, press_tag in zip(soup.select('.news_tit'), soup.select('.info_group')):
            # print(link, press_tag)
            press_name = press_tag.find('a', {'class': 'press'}).get_text(strip=True)
            
            try:
                article_response = requests.get(link['href'])
                article_response.raise_for_status()
            except requests.exceptions.HTTPError as http_err:
                print(f"HTTP 에러 발생: {http_err}")
            except requests.exceptions.RequestException as req_err:
                print(f"요청 에러 발생: {req_err}")
            except Exception as err:
                print(f"다른 에러 발생: {err}")

            # 기사 페이지에서 메타 태그 추출
            article_soup = BeautifulSoup(article_response.content, 'html.parser')
            meta_tag = article_soup.find('meta', {'property': 'article:published_time'})

            if meta_tag and 'content' in meta_tag.attrs:
                published_time = meta_tag['content']
                print(published_time)
                published_time = convert_to_isoformat(published_time)
                # print(published_time)

                try:
                    article_date = datetime.fromisoformat(published_time).date()
                    # article_date = str(article_date)

                    if three_days_ago <= article_date <= today:
                        print(f"기사의 발행 날짜는 오늘({article_date})로 최근 3일 이내입니다.")
                        print((link['href'], press_name))
                        if preferred_press is None or press_name in preferred_press:
                            article_urls.append((link['href'], press_name, article_date))
                except ValueError as e:
                    print(f"발행 날짜 정보를 찾을 수 없습니다. {e}")
                except TypeError as e:
                    print(f"발행 날짜 정보를 찾을 수 없습니다. {e}")

        
    print(f"Number of articles: {len(article_urls)}")
    return article_urls

def monitor_naver_news(keywords, preferred_press=None):
    for keyword in keywords:
        print(f"\n키워드 '{keyword}'에 대한 뉴스 검색 결과:\n")
        article_urls = search_naver_news(keyword, preferred_press)
        for url, press_name, article_date in article_urls:
            print(f"기사 URL: {url} (출처: {press_name})")
            news, title, content = extract_naver_news(url, press_name, article_date)

def main():
    # 입력 키워드와 신문사를 변경하고 싶으면 아래 코드를 수정하세요.
    keywords = ['신용카드', '카드론', '카드대출', '카드페이먼트']

    preferred_press = ['경향신문', '국민일보', '동아일보', '서울신문', '세계일보', '조선일보', '중앙일보', '한겨레', 
                       '한국일보', '디지털타임스', '매일경제', '머니투데이', '서울경제', '이데일리', '이투데이', '전자신문', '파이낸셜뉴스', '한국경제']

    monitor_naver_news(keywords, preferred_press)

if __name__ == "__main__":
    main()
