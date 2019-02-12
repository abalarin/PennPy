from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, session, logging, send_from_directory
from passlib.hash import sha256_crypt
import uuid, os

# Homebuilt imports
from PennPy import mysql
from PennPy.users.forms import (RegisterForm)
from PennPy.products.routes import get_products
from PennPy.models import Users
from PennPy.forms import RegistrationForm

users = Blueprint('users', __name__)

@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if request.method == 'GET':
        return render_template('sql.html', form=form)

    # Uses WTF to check if POST req and form is valid
    if form.validate_on_submit():
        if user_exsists(form.username.data, form.email.data):
            flash(f'{form.username.data} already exsists!', 'danger')
            return render_template('sql.html', form=form)
        else:
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('main.index'))

    return render_template('sql.html', form=form)

def user_exsists(username, email):
    # Get all Users in SQL
    users = Users.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False

# @users.route('/register', methods=['GET', 'POST'])
# def register():
#   form = RegisterForm(request.form)
#   if request.method == 'POST' and form.validate():
#
#       # Create SQL form data
#       name = form.name.data
#       email = form.email.data
#       username = form.username.data
#       password = sha256_crypt.encrypt(str(form.password.data))
#
#       # Create Cursor
#       cur = mysql.connection.cursor()
#
#       # Search for exsisting users
#       result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
#
#       # If no user exsists add user to DB
#       if result == 0:
#           cur.execute("INSERT INTO users(name, email, username, password, admin_level) VALUES(%s, %s, %s, %s, %s)", (name, email, username, password, 0))
#           mysql.connection.commit()
#           cur.close()
#           flash('You are now regiestered and can login!', 'success')
#       else:
#           flash('User Already Exsists!', 'danger')
#
#       return render_template('register.html', form=form)
#
#   elif request.method == 'GET':
#       return render_template('register.html', form=form)

@users.route('/login', methods=['POST'])
def login():
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
        cur.close()

        # Compare Password with crypt/hash module
        if sha256_crypt.verify(password_candidate, password):
            # Init session vars
            session['logged_in'] = True
            session['username'] = username
            session['admin_level'] = data['admin_level']

            flash('Successful Login!', 'success')
            return redirect(url_for('users.dashboard'))
            # app.logger.info('PASSS MATCH')

        else:
            flash('Login Not Successful!', 'danger')
            return redirect(url_for('users.dashboard'))

    else:
        flash('No user found!', 'danger')
        return redirect(url_for('main.index', error="No users found"))

    # Return an html template filled with form data
    return redirect(url_for('main.index', success="Logged In!"))

@users.route('/logout')
def logout():
  session.clear()
  flash('Youve logged out!', 'success')
  return redirect(url_for('main.index'))

@users.route('/profile')
def profile():
    if 'username' in session:
        user = get_user(session['username'])
        return render_template("profile.html", user = user)
    else:
        return redirect(url_for('main.index'))

@users.route('/dashboard')
def dashboard():
    if 'username' in session:
        user = get_user(session['username'])
        if user['admin_level'] > 0:
            return render_template("dashboard.html", products = get_products())
        else:
            return redirect(url_for('main.index'))
    else:
        return redirect(url_for('main.index'))

def get_user(username):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM users WHERE username = %s", [username])
    if result > 0:
        user = cur.fetchone()
        print(user)
        return user
