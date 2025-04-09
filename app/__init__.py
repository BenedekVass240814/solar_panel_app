from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate  # Import Migrate
import os

# Initialize the database and migrate object
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Set up configuration
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite for now, change to Postgres if needed
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize the database and migration
    db.init_app(app)
    migrate.init_app(app, db)  # Bind Flask-Migrate to your app and database

    # Import and register the routes
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
