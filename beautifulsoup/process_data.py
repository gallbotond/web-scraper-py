import json

def process_name(name):
    return name.replace('\u2122', '').replace('\u00ae', '').strip()

# "1.071,00 Lei" -> "1.071,00" float
def process_price(price):
    return float(price.split(' ')[0].replace('.', '').replace(',', '.'))

processed_data = []
# read the data from the file
with open('unprocessed_data.json', 'r') as file:
    unprocessed_data = json.load(file)
    
    for item in unprocessed_data:
        # process the item
        name = process_name(item['name'])
        price = process_price(item['price'])
        url = item['url']
        processed_data.append({
            'name': name,
            'price': price,
            'url': url
        })

# write the processed data to a file as json
with open('processed_data.json', 'w') as file:
    json.dump(processed_data, file)