import logging
from flask import Flask
from config import Config
from api.routes import main_bp

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
app.config.from_object(Config)

Config.validate()

app.register_blueprint(main_bp)


if __name__ == '__main__':
    app.run(debug=app.config['DEBUG'])
