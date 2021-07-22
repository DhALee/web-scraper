import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}


def get_last_page(url):
    url = requests.get(url, headers=HEADERS)
    # print(url) # 200 means okay

    soup = BeautifulSoup(url.text, "html.parser")
    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)


def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company, location = html.find(
        "h3", {"class": "mb4"}).find_all("span", recursive=False)
    company, location = company.get_text(
        strip=True), location.get_text(strip=True)
    job_id = html["data-jobid"]
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs?id={job_id}&q=python"
    }


def extract_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        print(f"Scrapping stackoverflow page: {page}")
        each_page = requests.get(f"{url}&pg={page + 1}")
        soup = BeautifulSoup(each_page.text, "html.parser")
        job_cards = soup.find_all("div", {"class": "-job"})
        for job_card in job_cards:
            job = extract_job(job_card)
            jobs.append(job)
    return jobs


def get_jobs(career):
    url = f"https://stackoverflow.com/jobs?q={career}"
    last_page = get_last_page(url)
    jobs = extract_jobs(last_page, url)
    return jobs
