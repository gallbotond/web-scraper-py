import json
import re

def process_name(name):
    return name.replace('\u2122', '').replace('\u00ae', '').strip()

# "1.071,00 Lei" -> "1.071,00" float
def process_price(price):
    num = re.search(r'\d.*\d', price).group()
    return float(num.replace('.', '').replace(',', '.'))

def process_rating(rating):
    return float(rating.split(' ')[0]) if rating else -1

def process_num_reviews(num_reviews):
    return int(num_reviews.replace('(', '').replace(')', '')) if num_reviews else 0

processed_data = []
# read the data from the file
with open('beautifulsoup/data/unprocessed_data.json', 'r') as file:
    unprocessed_data = json.load(file)
    
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
with open('beautifulsoup/data/processed_data.json', 'w') as file:
    json.dump(processed_data, file)