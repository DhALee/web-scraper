# Installed library -> resquests, beautifulsoup4
import requests

indeed_url = requests.get("https://kr.indeed.com/jobs?q=python&l=")

print(indeed_url) # 200 means okay
# print(indeed_url.text)