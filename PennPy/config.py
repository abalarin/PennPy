import os


class Config:

    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SECRET_KEY = os.environ.get('SECRET_KEY')

    # MYSQL init
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://' + DB_USER + ':' + DB_PASS + '@localhost:3306/PennPy'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Does this do anything?
    static_folder = 'images'

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
