# Install library -> resquests, beautifulsoup4
import requests
from bs4 import BeautifulSoup

RADIUS = 100
LIMIT = 50
URL = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=Python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius={RADIUS}&l=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%95%88%EC%96%91&fromage=any&limit={LIMIT}&sort=&psf=advsrch&from=advancedsearch"


def extract_indeed_pages():
    url = requests.get(URL)
    # print(url) # 200 means okay
    soup = BeautifulSoup(url.text, "html.parser")
    pagination = soup.find("div", {"class": "pagination"})

    links = pagination.find_all("a")
    pages = []
    for link in links[:-1]:  # To elimiante last element
        pages.append(int(link.find("span").string))
    max_page = pages[-1]
    return max_page


def extract_job(html):
    spans = html.find_all("span")
    for span in spans:
        if span.get("title") is not None:
            title = span.get("title")
    company = html.find("span", {"class": "companyName"}).string
    location = html.find("div", {"class": "companyLocation"}).string
    job_id = html.find_parent("a")["data-jk"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=Python&as_phr&as_any&as_not&as_ttl&as_cmp&jt=all&st&salary&radius=100&l=%EA%B2%BD%EA%B8%B0%EB%8F%84%20%EC%95%88%EC%96%91&fromage=any&limit=50&sort&psf=advsrch&from=advancedsearch&vjk={job_id}"
    }


def extract_indeed_jobs(last_page):
    jobs = []
    for page in range(last_page):
        # print(f"Scrapping page {page}")
        each_page = requests.get(f"{URL}&start={page * LIMIT}")
        soup = BeautifulSoup(each_page.text, "html.parser")
        job_cards_zone = soup.find("div", {"id": "mosaic-zone-jobcards"})
        job_cards = job_cards_zone.find_all(
            "div", {"class": "job_seen_beacon"})
        # print(len(job_cards)) # 50 job cards in a page
        for job_card in job_cards:
            job = extract_job(job_card)
            jobs.append(job)
    return jobs
