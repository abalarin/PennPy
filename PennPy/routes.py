# A Circular import, importing __init__.py
from PennPy import app

import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, send_from_directory

# SQL
from flask_mysqldb import MySQL

# FORMS Requirments
# from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Password hasher
from passlib.hash import sha256_crypt

#-- Object from hardscripted db <-- removing this and data.py
from PennPy.data import Products
Products = Products()
#-- end hardcode db

# Bootstrap(app)

# MYSQL init
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='linode!'
app.config['MYSQL_DB']='PennPy'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

# App seceret key for session
app.secret_key='secret123'


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# ----- Routes -----
@app.route('/')
def index():
  return render_template("index.html", products = Products)

@app.route('/dashboard')
def dashboard():
  return render_template("dashboard.html")

@app.route('/upload', methods=['POST'])
def upload():

  # Create a target path for new product image(s)
  target = os.path.join(APP_ROOT, 'static/images')
  print("IMG: " + target)

  # Create SQL Product Object
  product_name = request.form.get('product_name')
  product_category = request.form.get('product_category')
  product_cost = request.form.get('product_cost')
  product_description = request.form.get('product_description')
  product_images = []

  # If not directory exsists create new one
  if not os.path.isdir(target):
      os.mkdir(target)

  # Loop through files to upload
  for file in request.files.getlist("product_images"):
      print(file)
      print("{} is the file name".format(file.filename))
      filename = file.filename
      destination = "/".join([target, filename])
      print(destination)
      file.save(destination)
      product_images.append(destination)



  flash('Image Uploaded!', 'success')
  return render_template("dashboard.html")

@app.route('/upload/<filename>')
def get_image(filename):
  return send_from_directory("/static/images", filename)

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

      # Search for exsisting users
      result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

      # If no user exsists add user to DB
      if result == 0:
          cur.execute("INSERT INTO users(name, email, username, password) VALUES(%s, %s, %s, %s)", (name, email, username, password))
          mysql.connection.commit()

          # Success Message
          flash('You are now regiestered and can login!', 'success')
      else:
          flash('User Already Exsists!', 'danger')

      # Close Connection
      cur.close()

      redirect(url_for('index'))

  # Return an html template filled with form data
  return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():

  # Create Login object from form data
  form = LoginForm(request.form)

  if request.method == 'POST':

      # Get Form DataRequired
      username = request.form['username']
      password_candidate = request.form['password']

      # Create Cursor
      cur = mysql.connection.cursor()

      # Query the user from SQL DB
      result = cur.execute("SELECT * FROM users WHERE username = %s", [username])

      # Check if user exsists
      if result > 0:

          #Get stored hash
          data = cur.fetchone()
          password = data['password']

          # Compare Password with crypt/hash module
          if sha256_crypt.verify(password_candidate, password):

              # Init session vars
              session['logged_in'] = True
              session['username'] = username

              flash('Successful Login!', 'success')
              return redirect(url_for('dashboard'))
              # app.logger.info('PASSS MATCH')
          else:
              flash('Login Not Successful!', 'danger')
              app.logger.info('BAD PASSWORD')

          # Close SQL connection
          cur.close()

      else:
          return render_template('login.html', form=form, error="No users found")

  # Return an html template filled with form data
  return render_template('login.html', form=form)

@app.route('/logout')
def logout():
  session.clear()
  flash('Youve logged out!', 'success')
  return redirect(url_for('login'))


# -- Account Creation and Validation Declerations --
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
# -----------------------------------------------------------