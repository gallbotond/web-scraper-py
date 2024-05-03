import os
import json
import datetime
import random
from pymongo import MongoClient

def put_data_in_db():
    path = 'data/processed_specs/'
    files = os.listdir(path)
    now = datetime.datetime.now()
    print(now)

    # read the files as json
    for file in files:
        with open(path + file, 'r') as f:
            data = json.load(f)
            for item in data:
                response = db_items.insert_one(item)
                if response.acknowledged:
                    print(f"Inserted {item['name']} into the database")
        print(f"Inserted items from {file} into the database")

def print_items():
    # read the data from the database
    items = db_items.find()
    for item in items:
        print(item['name'])
        
    # print the number of items in the database
    print(db_items.count_documents({}), "items in the database")
        
def add_mock_prices():
    for item in db_items.find():
        item['price'] = [item['price']]
        # print(item['price'])
        for i in range(5):
            new_price = item['price'][0]['value'] * random.uniform(0.8, 1.1)
            new_date = datetime.datetime.now() - datetime.timedelta(days=(i + 1))
            # print(f"Updating price to {new_price} on {new_date}")
            item['price'].append({'value': new_price, 'date': new_date.strftime("%Y_%m_%d %H:%M:%S")})
        # print(item['price'])
        # update the item
        res = db_items.update_one({'_id': item['_id']}, {'$set': {'price': item['price']}})
        if res.acknowledged:
            print(f"Updated {item['name']}")
            
client = MongoClient('localhost', 27017)
db = client.mydb

db_items = db.items
