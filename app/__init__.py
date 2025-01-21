from flask_cors import CORS
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from .dynamic_api import dynamic_api
from .pastebin_api import pastebin_api
from flask_migrate import Migrate

# Initialize the extensions
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize db and migrate with app
    db.init_app(app)
    migrate.init_app(app, db) 
    
    # Enable CORS for all origins (or specify origins as needed)
    CORS(app, origins="*")
    
    # Register Blueprints
    app.register_blueprint(pastebin_api)
    app.register_blueprint(dynamic_api)
    
    return app
