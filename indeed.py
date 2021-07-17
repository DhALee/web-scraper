# Installed library -> resquests, beautifulsoup4
import requests
from bs4 import BeautifulSoup

RADIUS = 100
LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=Python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius={RADIUS}&l=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%95%88%EC%96%91&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"

def extract_indeed_pages():
    url = requests.get(URL)
    # print(url) # 200 means okay
    soup = BeautifulSoup(url.text, "html.parser")
    # print(soup)
    pagination = soup.find("div", {"class": "pagination"})
    # print(pagination)

    links = pagination.find_all("a")
    # print(links)
    pages = []
    for link in links[:-1]: # to elimiante last element
        pages.append(int(link.find("span").string))
    # print(pages)
    max_page = pages[-1]
    return max_page

def extract_indeed_jobs(last_page):
    jobs = []
    # for page in range(last_page):
    #     each_page = requests.get(f"{URL}&start={page * LIMIT}")
    #     # print(each_page.status_code)
    #     soup = BeautifulSoup(each_page.text, "html.parser")
    #     results = soup.find_all("div", {"class": "job_seen_beacon"})
    #     print(results)

    # each_page = requests.get(f"{URL}&start={0 * LIMIT}")
    # soup = BeautifulSoup(each_page.text, "html.parser")
    # results = soup.find_all("div", {"class": "job_seen_beacon"})
    # for result in results:
    #     spans = result.find("span")["title"]
    #     # print(spans.find("title"))
    #     print(spans)
    # # print(results)

    each_page = requests.get(f"{URL}&start={0 * LIMIT}")
    soup = BeautifulSoup(each_page.text, "html.parser")
    results = soup.find_all("h2", {"class": "jobTitle jobTitle-color-purple"})
    for result in results:
        spans = result.find("span")["title"]
        # print(spans.find("title"))
        print(spans)
    # print(results)

    return jobs
