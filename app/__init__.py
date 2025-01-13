from flask_cors import CORS
from flask import Flask
from .dynamic_api import dynamic_api
def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(dynamic_api)
    return app
