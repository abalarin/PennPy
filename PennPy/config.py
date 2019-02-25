import paypalrestsdk
import os


class Config:

    DB_USER = os.environ.get('DB_USER')
    DB_PASS = os.environ.get('DB_PASS')
    SECRET_KEY = os.urandom(12)

    # Connection to Postgres server
    SQLALCHEMY_DATABASE_URI = 'postgresql://' + DB_USER + ':' + DB_PASS + '@45.33.79.194:5432/PennPy'

    # Connection to local postgres db
    # SQLALCHEMY_DATABASE_URI = 'postgresql://abalarin:lindoe!@localhost:5432/PennPy'

    # To suppress FSADeprecationWarning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Gets pwd and declares it is the root dir for the App
    APP_ROOT = os.path.dirname(os.path.abspath(__file__))

    # PayPal sandbox config
    paypalrestsdk.configure({
        "mode": "sandbox",  # sandbox or live
        "client_id": os.environ.get('PAYPAL_CLIENT_ID'),
        "client_secret": os.environ.get('PAYPAL_CLIENT_SECRET')})
