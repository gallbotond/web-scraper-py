import requests
import time
from bs4 import BeautifulSoup

url = 'https://www.emag.ro/laptop-gaming-asus-rog-flow-x16-gv601vi-cu-procesor-intelr-coretm-i9-13900h-pana-la-5-40-ghz-16-qhd-mini-led-touch-16gb-1tb-ssd-nvidiar-geforce-rtxtm-4070-8gb-gddr6-tgp-120w-windows-11-pro-off-black-g/pd/DHNP8TYBM/'


# result = requests.get(url)
# while result.status_code != 200:
#     print(f"Failed to get data: {result.status_code}")
#     time.sleep(1)
# parse the html
# content = result.content
# read the html from a file
with open('./data/html/html.html', 'r') as file:
    content = file.read()
soup = BeautifulSoup(content, 'html.parser')

# save the html
# with open('beautifulsoup\data\html.html', 'w', encoding='utf-8') as file:
#     file.write(soup.prettify())

specs_tables = soup.find_all('table', class_='specifications-table')
specs_titles = soup.find_all('p', class_='pad-top-sm text-uppercase strong')
print(len(specs_tables), len(specs_titles))