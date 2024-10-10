import json
import logging
from marshmallow import Schema, fields

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ItemSchema(Schema):
    name = fields.String(required=True)
    description = fields.String(required=False)


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)


def load_data():
    try:
        with open('data.json', 'r') as data_file:
            return json.load(data_file)
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return []


def save_data(items):
    try:
        with open('data.json', 'w') as data_file:
            json.dump(items, data_file)
    except Exception as e:
        logging.error(f"Error saving data: {e}")
