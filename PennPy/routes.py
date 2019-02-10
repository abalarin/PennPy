# A Circular import, importing __init__.py
from PennPy import app
import uuid

import os
from flask import Flask, render_template, flash, request, redirect, url_for, session, logging, send_from_directory

# SQL
from flask_mysqldb import MySQL

# FORMS Requirments
# from flask_bootstrap import Bootstrap
from wtforms import Form, StringField, TextAreaField, PasswordField, validators

# Password hasher
from passlib.hash import sha256_crypt

# Bootstrap(app)

# MYSQL init
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='linode!'
app.config['MYSQL_DB']='PennPy'
app.config['MYSQL_CURSORCLASS']='DictCursor'

mysql = MySQL(app)

app.config['static_folder']='images'

# App seceret key for session
app.secret_key='secret123'


APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# ----- Routes -----
@app.route('/')
def index():
  return render_template("index.html", products = get_products())

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html", products = get_products())

@app.route('/upload', methods=['POST'])
def upload():
    # Create SQL Product Object
    product_id = str(id_validator(uuid.uuid4()))
    product_name = request.form.get('product_name')
    product_category = request.form.get('product_category')
    product_price = request.form.get('product_cost')
    product_description = request.form.get('product_description')
    image_root = "images/" + product_id + "/"

    # Create a target path for new product image(s)
    target = os.path.join(APP_ROOT, 'static/images/' + product_id)

    # If not directory exsists create new one
    if not os.path.isdir(target):
        os.mkdir(target)

    # Loop through files to upload
    for file in request.files.getlist("product_images"):
        print("{} is the file name".format(file.filename))
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    cur = mysql.connection.cursor()

    cur.execute("INSERT INTO product(name, category, price, description, image_root, id) VALUES(%s, %s, %s, %s, %s, %s)", (product_name, product_category, product_price, product_description, image_root, product_id))
    mysql.connection.commit()
    cur.close()

    flash('Image Uploaded!', 'success')
    return url_for('dashboard')

@app.route('/image/<filename>')
def get_image(filename):
    return send_from_directory('static/images', filename)

@app.route('/image/<id>')
def get_images(id):
    target = os.path.join(APP_ROOT, 'static/images/' + id)
    if os.path.isdir(target):
        images = os.listdir(target)
        return images

    return render_template('index.html', error="No images")

@app.route('/product/products', methods=['GET'])
def get_products():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()

    # for product in products:
    #     # files = os.listdir("./static/images/" + product["name"])
    #     target = os.path.join(APP_ROOT, 'static/images/' + str(product["id"]))
    #     if os.path.isdir(target):
    #         img_names = os.listdir(target)
    #         print("imgs ----- ")
    #         print(img_names)
    #         # for item in
        # print(os.listdir("./static/images/" + product["name"]))

    # print(products)
    return (products)

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
  if request.method == 'POST':

      # Get Form DataRequired
      username = request.form.get('username')
      password_candidate = request.form.get('password')

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
          flash('No user found!', 'danger')
          return redirect(url_for('index', error="No users found"))

      # Return an html template filled with form data
      return redirect(url_for('index', success="Logged In!"))

@app.route('/logout')
def logout():
  session.clear()
  flash('Youve logged out!', 'success')
  return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

def id_validator(uid):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM product WHERE id = %s", [uid])
    cur.close()

    if result > 0:
        id_validator(uuid.uuid4())

    return uid

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

# -----------------------------------------------------------
