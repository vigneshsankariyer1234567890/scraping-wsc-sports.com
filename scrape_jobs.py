import requests
import csv
from bs4 import BeautifulSoup

WSC_URL = "https://wsc-sports.com/careers/"

WSC_page = requests.get(WSC_URL)

careers_soup = BeautifulSoup(WSC_page.content,"html.parser")

# find the relevant urls of the positions
url_results = careers_soup.find(id="d").find_all('a', href=True)

# container to store our result dictionary
results_container = []

# href does not contain https, need prefix to send get request to page
base_str = "https:"

for a in url_results:
    url = base_str + a['href']
    job_soup = BeautifulSoup(requests.get(url).content,"html.parser")

    # find the name of the position
    position_name_element = job_soup.find("h2", class_="comeet-position-name")

    # find the inforation about the position
    position_info_element = job_soup.find("div", class_="comeet-position-description comeet-user-text").find("li")

    # create a container for relevant data, dummy index since we need to sort 
    dict = {
        'index': 0,
        'position name': position_name_element.text.strip(),
        'position info': position_info_element.text.strip()
    }
    results_container.append(dict)

# sort by position name
sorted_results = sorted(results_container, key=lambda d: d['position name'])

index = 1

for pos in sorted_results:
    pos['index'] = index
    index+=1

keys = sorted_results[0].keys()

# write to ./jobs.csv
with open('./jobs.csv', 'w', newline='') as output_file:
    dict_writer = csv.DictWriter(output_file, keys)
    dict_writer.writeheader()
    dict_writer.writerows(sorted_results)
