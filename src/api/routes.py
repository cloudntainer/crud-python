from flask import Blueprint, request, jsonify
from .items import load_data, save_data, item_schema, items_schema
from marshmallow import ValidationError
import logging
from .exceptions import (
    ItemNotFoundError,
    ItemAlreadyExistsError,
    ItemNameTooShortError
)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET'])
def index():
    return jsonify({"message": "Welcome to the API!"}), 200


@main_bp.route('/api/items', methods=['GET'])
def get_items():
    items = load_data()
    logging.info("GET /api/items - Items retrieved successfully")
    return jsonify(items_schema.dump(items)), 200


@main_bp.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    items = load_data()
    if item_id < 0 or item_id >= len(items):
        logging.warning("GET /api/items/%d - Item not found", item_id)
        raise ItemNotFoundError(f"Item with id {item_id} not found.")
    return jsonify(item_schema.dump(items[item_id])), 200


@main_bp.route('/api/items', methods=['POST'])
def add_item():
    try:
        new_item = item_schema.load(request.json)
        items = load_data()

        for item in items:
            if item['name'] == new_item['name']:
                logging.warning(
                    "POST /api/items - Item already exists: %s",
                    new_item['name']
                )
                raise ItemAlreadyExistsError(
                    new_item[
                        'name'
                    ]
                )

        if len(new_item['name']) < 3:
            logging.warning(
                "POST /api/items - Item name too short: %s",
                new_item['name']
            )
            raise ItemNameTooShortError(new_item['name'])

        items.append(new_item)
        save_data(items)

        logging.info("POST /api/items - Item added successfully: %s", new_item)
        return jsonify(
            {
                "message": "Item added successfully",
                "item": item_schema.dump(new_item)
            }
        ), 201
    except ItemAlreadyExistsError as e:
        logging.error("Item already exists: %s", str(e))
        return jsonify({"error": "Item already exists"}), 400
    except ItemNameTooShortError as e:
        logging.error("Item name too short: %s", str(e))
        return jsonify(
            {
                "error": "Item name must be at least 3 characters long"
            }
        ),
        400
    except ValidationError as err:
        logging.error("Validation error: %s", err.messages)
        return jsonify({"errors": err.messages}), 400
    except Exception as e:
        logging.error("Error saving to JSON: %s", str(e))
        return jsonify({"error": "Internal Server Error"}), 500


@main_bp.route('/api/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    items = load_data()
    if item_id < 0 or item_id >= len(items):
        logging.warning("PUT /api/items/%d - Item not found", item_id)
        raise ItemNotFoundError(f"Item with id {item_id} not found.")

    try:
        updated_item = item_schema.load(request.json)
        items[item_id] = updated_item
        save_data(items)

        logging.info(
            "PUT /api/items/%d - Item updated successfully: %s",
            item_id,
            updated_item
        )
        return jsonify(
            item_schema.dump(
                updated_item
            )
        ),
        200
    except ValidationError as err:
        logging.error(
            "Validation error: %s",
            err.messages
        )
        return jsonify(
            {
                "errors": err.messages
            }
        ),
        400
    except Exception as e:
        logging.error(
            "Error saving to JSON: %s",
            str(
                e
            )
        )
        return jsonify(
            {
                "error": "Internal Server Error"
            }
        ),
        500


@main_bp.route('/api/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    items = load_data()

    if item_id < 0 or item_id >= len(items):
        logging.warning("DELETE /api/items/%d - Item not found", item_id)
        raise ItemNotFoundError(f"Item with id {item_id} not found.")

    try:
        deleted_item = items.pop(item_id)
        save_data(items)

        logging.info(
            "DELETE /api/items/%d - Item deleted successfully: %s",
            item_id,
            deleted_item
        )
        return jsonify(
            {
                "message": "Item deleted successfully",
                "item": deleted_item
            }
        ),
        200
    except Exception as e:
        logging.error(
            "Error during item deletion: %s",
            str(
                e
            )
        )
        return jsonify(
            {
                "error": "Internal Server Error"
            }
        ),
        500
