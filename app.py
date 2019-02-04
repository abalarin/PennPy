from flask import Flask, render_template, flash, request, redirect, url_for, session, logging

from flask_nav import Nav
from flask_nav.elements import Navbar, View

from flask_mysqldb import MySQL

# - FORMS
from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, TextAreaField, PasswordField, validators
from passlib.hash import sha256_crypt

#Object from hardscripted db
from data import Products
Products = Products()


# Creating a navbar object
topbar = Navbar('MyBar',
    View('Home', 'index'),
    View('Profile', 'profile'),
    View('Login', 'login'),
    View('Register', 'register')
)

class RegisterForm(Form):
    name = StringField('Name', [validators.Length(min=1, max=50)])
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email', [validators.Length(min=4, max=50)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Pass dont match')
    ])
    confirm = PasswordField('Confirm Password')

class LoginForm(Form):
    username = StringField('Username', [validators.Length(min=1, max=25)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=1, max=50)])



def create_app():

  #Instantiate Application
  app = Flask(__name__)
  Bootstrap(app)

  # NAV Bar config
  nav = Nav()
  nav.register_element('top', topbar)

  # [...]
  # later on, initialize your app:
  nav.init_app(app)

  # #MYSQL init
  app.config['MYSQL_HOST']='localhost'
  app.config['MYSQL_USER']='root'
  app.config['MYSQL_PASSWORD']='linode!'
  app.config['MYSQL_DB']='PennPy'
  app.config['MYSQL_CURSORCLASS']='DictCursor'

  mysql = MySQL(app)

  app.secret_key='secret123'


  # Routes
  @app.route('/')
  def index():
      # cur = mysql.connection.cursor()
      # cur.execute('''SELECT user, host FROM mysql.user''')
      # rv = cur.fetchall()

      return render_template("index.html", products = Products)

  @app.route('/profile')
  def profile():
      return render_template("profile.html")

  @app.route('/register', methods=['GET', 'POST'])
  def register():
      form = RegisterForm(request.form)
      if request.method == 'POST' and form.validate():

          # Create SQL form data
          name = form.name.data
          email = form.email.data
          username = form.username.data
          password = sha256_crypt.encrypt(str(form.password.data))

          # Create Cursor
          cur = mysql.connection.cursor()

          cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))

          # Commit to DB
          # mysql.connection.commit()

          # Close Connection
          cur.close()

          # Success Message
          flash('You are now regiestered and can login', 'scucess')

          redirect(url_for('index'))

      return render_template('register.html', form=form)

  @app.route('/login', methods=['GET', 'POST'])
  def login():
      form = LoginForm(request.form)
      if request.method == 'POST':
          # Get Form DataRequired
          username = request.form['username']
          password_candidate = request.form['password']

          # Create Cursor
          cur = mysql.connection.cursor()

          # Query the user from SQL DB
          result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

          if result > 0:
              #Get stored hash
              data = cur.fetchone()
              password = data['password']

              # Compare Password
              if sha256_crypt.verify(password_candidate, password):
                  app.logger.info('PASSS MATCH')
          else:
              app.logger.info('NO USERS')

      return render_template('login.html', form=form)

  return app
