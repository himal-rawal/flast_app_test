from flask import Flask
from .dynamic_api import dynamic_api

def create_app():
    app = Flask(__name__)

    # Attach the app instance to the blueprint
    dynamic_api.app = app

    # Register the blueprint
    app.register_blueprint(dynamic_api)

    return app
