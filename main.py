import requests
from bs4 import BeautifulSoup

URL = 'https://www.yell.com/ucs/UcsSearchAction.do?'

params = {
    'scrambleSeed': '973393193',
    'keywords':	'Hotels',
    'location':	'new york',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',

}

result = []

res = requests.get(URL, params=params, headers=headers)
soup = BeautifulSoup(res.text, 'html.parser')

print(res.status_code)
# scraping process
headers_contents = soup.find_all('div', {'class': 'row businessCapsule--mainRow'})

for content in headers_contents:
    title = content.find('h2', {'class': 'businessCapsule--name'}).text
    classification = content.find('span', {'class':'businessCapsule--classification'}).text
    link_web = content.find('div', {'class':'businessCapsule--ctas'}).find('a')['href']
    # sorting data
    print(title)
    data_dict = {
        'title': title,
        'classification': classification,
        'link_web': link_web,
    }
    print(data_dict)
    result.append(data_dict)

print("jumlah datanya adalah", len(result))
