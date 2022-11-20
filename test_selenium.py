from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from bs4 import BeautifulSoup
import os
import json
import pandas as pd
from selenium.webdriver.chrome.options import Options

yell = "https://www.yell.com"
URL = "/ucs/UcsSearchAction.do?keywords=Restaurants&location=London&scrambleSeed=1941023813"

service = Service(executable_path="C:\Development\chromedriver.exe")
options = Options()
options.add_argument('--incognito')
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=service, options=options)

driver.get(yell + URL)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'lxml')

result = []
header_contents = soup.find_all('div', class_='row businessCapsule--mainRow')

for content in header_contents:
    title = content.find('h2', class_='businessCapsule--name').text
    classification = content.find('span', class_='businessCapsule--classification').text
    try:
        # we want to check the existence of link
        link_web = content.find('div', class_='businessCapsule--ctas').find_all('a', class_="btn btn-yellow businessCapsule--ctaItem")[-1]['href']
        if "http" not in link_web:
            link_web = None
    except Exception:
        link_web = None
    telephone = content.find('span', class_='business--telephoneNumber').text
    # sorting data

    final_data = {
        'title': title,
        'classification': classification,
        'link_web': link_web,
        'telephone': telephone,
    }
    #print(final_data)
    result.append(final_data)
print(f"successfully scrape page 1")

# list of the next pages
next_page = soup.find('div', class_='col-sm-14 col-md-16 col-lg-14 text-center').find_all('a', class_='btn btn-grey')
pages_list = []
for page in next_page:
    pages_list.append(page['href'])

# scraping process for subsequence pages until page 10
for page in range(len(next_page)):

    driver.get(yell + pages_list[page])
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'lxml')

    header_contents = soup.find_all('div', class_='row businessCapsule--mainRow')

    for content in header_contents:
        title = content.find('h2', class_='businessCapsule--name').text
        classification = content.find('span', class_='businessCapsule--classification').text
        try:
            # we want to check the existence of link
            link_web = content.find('div', class_='businessCapsule--ctas').find_all('a', class_="btn btn-yellow businessCapsule--ctaItem")[-1]['href']
            telephone = content.find('span', class_='business--telephoneNumber').text
            if "http" not in link_web:
                link_web = None
        except Exception:
            link_web = None
            telephone = None


        # sorting data

        final_data = {
            'title': title,
            'classification': classification,
            'link_web': link_web,
            'telephone': telephone,
        }
        #print(final_data)
        result.append(final_data)
    print(f"successfully scrape page {page+2}")

try:
    os.mkdir('json_result')
except FileExistsError:
    pass
with open('json_result/final_data.json', "w+") as json_data:
    json.dump(result, json_data)
print('json created')

# create csv
df = pd.DataFrame(result)
df.to_csv('yell_data.csv', index=False)
df.to_excel('yell_data.xlsx', index=False)
print("Data created success")
print("Total rows", len(result))
