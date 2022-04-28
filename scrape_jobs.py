import requests
from bs4 import BeautifulSoup

WSC_URL = "https://wsc-sports.com/careers/"

WSC_page = requests.get(WSC_URL)

careers_soup = BeautifulSoup(WSC_page.content,"html.parser")

url_results = careers_soup.find(id="d").find_all('a', href=True)

url_container = []

for a in url_results:
    url_container.append(a['href'])

for url in url_container:
    page = requests.get(url)
    job_soup = BeautifulSoup(page.content,"html.parser")

