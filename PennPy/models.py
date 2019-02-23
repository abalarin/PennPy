# --------------------------------------------
# Move into respective endpoints
# --------------------------------------------
from sqlalchemy.sql import func
from PennPy import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    register_date = db.Column(db.DateTime(
        timezone=True), server_default=func.now())
    admin_level = db.Column(db.Integer, default=0)
    addresses = db.relationship('Address', backref='user')

    def __repr__(self):
        return(self.username + ", " + self.email)


class Product(db.Model):
    id = db.Column(db.String(255), unique=True, primary_key=True)
    name = db.Column(db.String(100))
    category = db.Column(db.String(100))
    price = db.Column(db.Integer)
    description = db.Column(db.String(255))

    def __repr__(self):
        return(self.name + ", " + self.category)


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    address1 = db.Column(db.String(255), nullable=False)
    address2 = db.Column(db.String(255))
    country = db.Column(db.String(255))
    state = db.Column(db.String(255))
    zipcode = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return(self.address1)
