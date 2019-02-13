import os


class Config:
    # MYSQL init
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root:linode!@localhost:3306/PennPy'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Removing after migrate to SQLAlchemy
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = 'linode!'
    MYSQL_DB = 'PennPy'
    MYSQL_CURSORCLASS = 'DictCursor'

    # Does this do anything?
    static_folder = 'images'

    # Change to envir var
    SECRET_KEY = 'secret123'

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
