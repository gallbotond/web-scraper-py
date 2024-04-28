import requests

from bs4 import BeautifulSoup

unprocessed_data = []

website = 'https://www.emag.ro/search/ryzen%209?ref=effective_search'
result = requests.get(website)
if result.status_code != 200:
    print(f"Failed to get data: {result.status_code}")
    exit()
content = result.content
soup = BeautifulSoup(content, 'html.parser')
cards = soup.find_all('div', class_='card-item')
print(f"Found {len(cards)} items")
for card in cards:
    try:
        name = card.find('a', class_='card-v2-title').text
        price = card.find('p', class_='product-new-price').text
        url = card.find('a', class_='card-v2-title')['href']
        unprocessed_data.append({
            'name': name,
            'price': price,
            'url': url
        })
        # print(f"Name: {name}")
        # print(f"Price: {price}")
        # print(f"URL: {url}")
    except AttributeError:
        print("Failed to parse item")
        continue
print(f"Processed {len(unprocessed_data)} items")

# write the data to a file as json
import json
with open('unprocessed_data.json', 'w') as file:
    json.dump(unprocessed_data, file)

