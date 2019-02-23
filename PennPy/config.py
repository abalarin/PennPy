import os


class Config:

    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SECRET_KEY = os.urandom(12)

    # MYSQL init
    # SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + \
    #     ':' + DB_PASS + '@45.33.79.194:5432/PennPy'

    SQLALCHEMY_DATABASE_URI = 'postgresql://abalarin:lindoe!@localhost:5432/PennPy'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Does this do anything?
    static_folder = 'images'

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
