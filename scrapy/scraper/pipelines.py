# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import logging
from itemadapter import ItemAdapter

class ScraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # Stripping whitespace from the name, price, and rating fields
        stripped_fields = ['name', 'price', 'rating']
        for field in stripped_fields:
            field_value = adapter.get(field)
            if isinstance(field_value, str):
                adapter[field] = field_value.strip()

        # Converting the price and rating field to a float
        float_fields = ['price', 'rating']
        for field in float_fields:
            field_value = adapter.get(field)
            if isinstance(field_value, str):
                try:
                    adapter[field] = float(field_value)
                except ValueError:
                    logging.warning(f"Failed to convert {field} to float: {field_value}")

        # Converting the num_reviews field to an integer
        num_reviews = adapter.get('num_reviews')
        if isinstance(num_reviews, str):
            try:
                adapter['num_reviews'] = int(num_reviews.replace('(', '').replace(' review-uri)', ''))
            except ValueError:
                logging.warning(f"Failed to convert num_reviews to integer: {num_reviews}")

        # Remove spaces from the end of each value in the specs field
        specs = adapter.get('specs')
        if isinstance(specs, dict):
            adapter['specs'] = {key.strip(): value.strip() for key, value in specs.items()}

        # Log the processed item
        logging.info("Processed item: %s", item)
        
        return item
