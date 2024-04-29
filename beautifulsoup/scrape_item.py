import time
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# helper functions
def process_value(value):
    return value.strip()

def process_technologies(value):
    return value.replace('\u2122', '').replace('\u00ae', '').strip().split('\n')

def process_specs(specs_table):
    specs = {}
    to_int = ["Numar nuclee", "Numar thread-uri"]
    split_nl = ["Putere termica (W)", "Continut pachet"]
    for row in specs_table.find_all('tr'):
        key = row.find('td', class_='col-xs-4').text
        value = row.find('td', class_='col-xs-8').text
        if key == 'Altele':
            specs[key] = process_technologies(value)
        elif key in to_int:
            specs[key] = int(value)
        elif key in split_nl:
            specs[key] = value.strip().split('\n')
        else:
            specs[key] = process_value(value)
    return specs

# parameters
items = []
blocked = 0

# read the data
with open('beautifulsoup\data\processed_data.json', 'r') as file:
    items = json.load(file)

blocked = 0
# fetch and process the result
for item in items:
    # fetch the page
    result = requests.get(item['url'])
    retry_time = 2
    retries = 0
    max_retries = 10
    # error handling and retries
    while result.status_code != 200 and retries < max_retries:
        print(f"Failed to get data: {result.status_code} {result.reason}")
        print(f"{retries}. Retrying in {retry_time} seconds...")
        time.sleep(retry_time)
        result = requests.get(item['url'])
        retries += 1
        retry_time *= 2
    blocked += retries
    if retries == max_retries:
        print(f"Failed to get data in {max_retries} retries")
        continue
    # parse the html
    content = result.content
    soup = BeautifulSoup(content, 'html.parser')
    specs_table = soup.find('table', class_='specifications-table')
    # process the specs
    item['specs'] = process_specs(specs_table)
    print(f"Processed {' '.join(item['name'].split(' ')[:5]).replace(',','')}...")
    time.sleep(0.3)

# write the processed data to a file as json
now = datetime.now().strftime("%H_%M_%S")
with open(f'beautifulsoup\data\processed_data_specs_{now}.json', 'w') as file2:
    json.dump(items, file2)
print(f"Processed {len(items)} items")
print(f"Blocked by eMAG: {blocked} times")