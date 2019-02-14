from flask import Flask, render_template, flash, redirect, url_for
from PennPy.config import Config
from flask_sqlalchemy import SQLAlchemy
from PennPy.endpoints.users.forms import RegistrationForm, LoginForm

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
    from PennPy.endpoints.products.routes import products
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(products)

    return app
