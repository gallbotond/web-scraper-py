import time
import requests
from bs4 import BeautifulSoup

# helper functions
def text_field(element):
    return element.text if element else ''

def link_field(element, type):
    return element[type] if element else ''

def scrape_page(website):
    result = requests.get(website)
    retry_time = 2
    retries = 0
    max_retries = 10

    # error handling and retries
    while result.status_code != 200 and retries < max_retries:
        print(f"Failed to get data: {result.status_code} {result.reason}")
        print(f"{retries}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        result = requests.get(website)
        retries += 1
        retry_time *= 2
    if retries == max_retries:
        print(f"Failed to get data in {max_retries} retries")
        
    # parse page
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    cards = soup.find_all('div', class_='card-item')
    pagination = soup.find_all('a', class_='js-change-page')
    print(f"Found {len(cards)} items")

    # extract the data
    for card in cards:
        name = text_field(card.find('a', class_='card-v2-title'))
        price = text_field(card.find('p', class_='product-new-price'))
        url = link_field(card.find('a', class_='card-v2-title'), 'href')
        rating = text_field(card.find('span', class_='average-rating'))
        num_reviews = text_field(card.find('span', class_='visible-xs-inline-block'))
        img = link_field(card.find('img'), 'src')
        unprocessed_data.append({
            'name': name,
            'price': price,
            'url': url,
            'rating': rating,
            'num_reviews': num_reviews,
            'img': img
        })
    print(f"Processed {len(unprocessed_data)} items at {website}")
    return pagination

def get_next_page(pagination):
    for page in pagination:
        if page.text == 'Pagina urmatoare':
            return page
    return None
    
# parameters
unprocessed_data = []
blocked = 0
search_term = 'ryzen 9'
website = f'https://www.emag.ro/search/{"+".join(search_term.split(" "))}'

while True:
    # print(website)
    pagination = scrape_page(website)
    next_page = get_next_page(pagination)
    time.sleep(5)
    if next_page:
        website = 'https://www.emag.ro' + next_page['href']
    else:
        break
    
# statistics
print("\n --- Summary ---\n")
print(f"Found {len(unprocessed_data)} items in total")
# print(f"Blocked by eMAG: {blocked} times")

file_path = 'beautifulsoup/data/unprocessed_data.json'
# write the data to a file as json
print(f"Writing {len(unprocessed_data)} items to {file_path}")
import json
with open(file_path, 'w') as file:
    json.dump(unprocessed_data, file)

