import requests
from bs4 import BeautifulSoup
import sys

URL = f"https://stackoverflow.com/jobs?q=python"
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def get_last_page():
    url = requests.get(URL, headers=HEADERS)
    # print(url) # 200 means okay

    soup = BeautifulSoup(url.text, "html.parser")

    # To check browser html and soup html same
    # with open("stackoverflow.html", "a", -1, 'utf-8') as f:
    #     f.write(str(soup))

    pages = soup.find("div", {"class": "s-pagination"}).find_all("a")
    last_page = pages[-2].get_text(strip=True)
    return int(last_page)

def extract_job(html):
    title = html.find("h2").find("a")["title"]
    company = html.find("h3").find("span").get_text(strip=True)
    location = html.find("h3").find("span", {"class": "fc-black-500"}).get_text(strip=True)
    job_id = html["data-jobid"]
    # print(title, company, location, job_id)
    return {
        'title': title,
        'company': company,
        'location': location,
        'link': f"https://stackoverflow.com/jobs?id={job_id}&q=python"
    }

def extract_jobs(last_page):
    jobs = []
    for page in range(last_page):
        each_page = requests.get(f"{URL}&pg={page + 1}")
        # print(each_page.status_code)
        soup = BeautifulSoup(each_page.text, "html.parser")
        job_cards = soup.find_all("div", {"class": "-job"})
        for job_card in job_cards:
            job = extract_job(job_card)
            jobs.append(job)
    return jobs


def get_jobs():
    last_page = get_last_page()
    jobs = extract_jobs(last_page)
    return jobs