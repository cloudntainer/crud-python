import os
import json
import logging
from flask import Flask
from api.routes import main_bp

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

app.config.from_object('config.Config')

data_file_path = os.path.join(
    os.path.dirname(
        os.path.dirname(__file__)
    ),
    'data.json'
)

if not os.path.exists(data_file_path):
    logger.error("Data file does not exist at path: %s", data_file_path)
    raise FileNotFoundError(f"Data file not found at {data_file_path}")

try:
    with open(data_file_path) as data_file:
        app.config['DATA'] = json.load(data_file)
        logger.info("Data loaded successfully.")
except FileNotFoundError as fnf_error:
    logger.error("Data file not found: %s", fnf_error)
    raise
except json.JSONDecodeError as json_error:
    logger.error("Error decoding JSON: %s", json_error)
    raise
except Exception as e:
    logger.error("Error loading data from JSON: %s", e)
    raise

app.register_blueprint(main_bp)

if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
