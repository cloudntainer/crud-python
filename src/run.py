import os
from flask import Flask
from api.routes import main_bp

app = Flask(__name__)

app.register_blueprint(main_bp)

if __name__ == "__main__":
    debug_mode = os.getenv('FLASK_DEBUG', '0') == '1'
    app.run(host='127.0.0.1', port=50010, debug=debug_mode)
