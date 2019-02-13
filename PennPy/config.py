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

    static_folder = 'images'

    SECRET_KEY = 'secret123'
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))
