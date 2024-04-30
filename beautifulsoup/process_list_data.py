import json
import re

def process_name(name):
    strings = ['\u2122', '\u00ae', '\uff0c', '\u1d49']
    for string in strings:
        name = name.replace(string, '')
    return name.strip()

def process_price(price):
    num = re.search(r'\d.*\d', price).group()
    return float(num.replace('.', '').replace(',', '.'))

def process_rating(rating):
    return float(rating.split(' ')[0]) if rating else -1

def process_num_reviews(num_reviews):
    return int(num_reviews.replace('(', '').replace(')', '')) if num_reviews else 0

def process_list_data(unprocessed_data=None, file_name=None):
    processed_data = []
    print(f"Processing {len(unprocessed_data)} items from {file_name}...")
    # read the data from the file
    # with open(f'beautifulsoup/data/unprocessed_list/{file_name}.json', 'r') as file:
    #     unprocessed_data = json.load(file)
        
    for item in unprocessed_data:
        if not item['name'] or not item['price']:
            continue
        name = process_name(item['name'])
        price = process_price(item['price'])
        url = item['url']
        rating = process_rating(item['rating'])
        num_reviews = process_num_reviews(item['num_reviews'])
        img = item['img']
        processed_data.append({
            'name': name,
            'price': price,
            'url': url,
            'rating': rating,
            'num_reviews': num_reviews,
            'img': img
        })

    # write the processed data to a file as json
    print(f"Done, writing {len(processed_data)} items to beautifulsoup/data/processed_list/{file_name}.json")
    with open(f'beautifulsoup/data/processed_list/{file_name}.json', 'w') as file:
        json.dump(processed_data, file)
        
    return processed_data