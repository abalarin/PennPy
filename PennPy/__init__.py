from flask import Flask
from flask_mysqldb import MySQL
from PennPy.config import Config

mysql = MySQL()

def create_app(config_class=Config):

    #Instantiate Application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init Mysql
    mysql.init_app(app)

    # import PennPy.routes
    from PennPy.main.routes import main
    from PennPy.users.routes import users
    from PennPy.products.routes import products
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(products)

    return app
