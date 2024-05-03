import time
import requests
import json
from bs4 import BeautifulSoup
from datetime import datetime

# helper functions
def process_value(value):
    return value.strip().replace('\u2122', '').replace('\u00ae', '').replace('\u00a0', '').replace('\u2013', '')

# TODO: process the specs with different parts
def process_specs(specs_table):
    specs = {}
    to_int = ["Numar nuclee", "Numar thread-uri"]
    for row in specs_table.find_all('tr'):
        key = row.find('td', class_='col-xs-4').text
        value = row.find('td', class_='col-xs-8').text
        if key in to_int:
            specs[key] = int(value)
        elif '\n' in value:
            specs[key] = process_value(value).split('\n')
        else:
            specs[key] = process_value(value)
    return specs

def scrape_process_item(processed_data, file_name):
    # parameters
    items = []
    blocked = 0

    # read the data
    # with open('beautifulsoup\data\processed_data.json', 'r') as file:
    #     items = json.load(file)
    items = processed_data

    blocked = 0
    # fetch and process the result
    for item in items:
        # fetch the page
        result = requests.get(item['url'])
        retry_time = 2
        retries = 0
        max_retries = 7
        sleep_time = 0.3
        # error handling and retries
        while result.status_code != 200 and retries < max_retries:
            print(f"Failed to get data: {result.status_code}, reason: {result.reason}")
            print(f"{retries}. Retrying in {retry_time} seconds...")
            time.sleep(retry_time)
            result = requests.get(item['url'])
            retries += 1
            retry_time *= 2
            sleep_time += 0.1
        blocked += retries
        if retries == max_retries:
            print(f"Failed to get data in {max_retries} retries")
            continue
        
        # parse the html
        content = result.content
        soup = BeautifulSoup(content, 'html.parser')
        specs_tables = soup.find_all('table', class_='specifications-table')
        specs_titles = soup.find_all('p.pad-top-sm.text-uppercase.strong')
        print(len(specs_tables), len(specs_titles))
        
        # process the specs
        for specs_table in specs_tables:
            specs = process_specs(specs_table)
            if(item.get('specs') == None):
                item['specs'] = [specs]
            else:
                item['specs'].append(specs)
                
        print(f"Processed {' '.join(item['name'].split(' ')[:8]).replace(',','')}...")
        print(f'Waiting {sleep_time} seconds...')
        time.sleep(0.3)

    # write the processed data to a file as json
    with open(f'beautifulsoup\data\processed_specs\{file_name}.json', 'w') as file2:
        json.dump(items, file2)
    
    # statistics
    print("\n --- Item Scraping Summary ---\n")
    print(f"Processed {len(items)} items")
    print(f"Blocked by eMAG: {blocked} times")