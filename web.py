# Installed library -> resquests, beautifulsoup4
import requests
from bs4 import BeautifulSoup

indeed_url = requests.get("https://kr.indeed.com/%EC%B7%A8%EC%97%85?as_and=python&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=100&l=%EA%B2%BD%EA%B8%B0%EB%8F%84+%EC%95%88%EC%96%91&fromage=any&limit=50&sort=&psf=advsrch&from=advancedsearch")
# print(indeed_url) # 200 means okay

indeed_soup = BeautifulSoup(indeed_url.text, "html.parser")
# print(indeed_soup)

pagination = indeed_soup.find("div", {"class": "pagination"})
# print(pagination)

links = pagination.find_all("a")
# print(links)

pages = []
for link in links[:-1]: # to elimiante last element
    pages.append(int(link.find("span").string))
# print(pages)
max_page = pages[-1]