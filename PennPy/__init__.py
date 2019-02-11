from flask import Flask, render_template, flash, redirect, url_for
from flask_mysqldb import MySQL
from PennPy.config import Config
from flask_sqlalchemy import SQLAlchemy
from PennPy.forms import RegistrationForm, LoginForm

mysql = MySQL()
db = SQLAlchemy()

class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    # image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

def create_app(config_class=Config):

    #Instantiate Application
    app = Flask(__name__)
    app.config.from_object(Config)

    # Init Mysql
    mysql.init_app(app)
    db.init_app(app)

    @app.route("/sql", methods=['GET', 'POST'])
    def register():
        print(Users.query.all())
        form = RegistrationForm()
        if form.validate_on_submit():
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('main.index'))
        return render_template('sql.html', title='Register', form=form)

    # import PennPy.routes
    from PennPy.main.routes import main
    from PennPy.users.routes import users
    from PennPy.products.routes import products
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(products)

    return app
