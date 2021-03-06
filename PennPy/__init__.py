from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from PennPy.config import Config

db = SQLAlchemy()


def create_app(config_class=Config):

    # Instantiate Application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init Mysql
    db.init_app(app)

    # Import and init Blueprints
    from PennPy.endpoints.main.routes import main
    from PennPy.endpoints.users.routes import users
    from PennPy.endpoints.listings.routes import listings
    from PennPy.endpoints.orders.routes import orders

    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(listings)
    app.register_blueprint(orders)

    return app
