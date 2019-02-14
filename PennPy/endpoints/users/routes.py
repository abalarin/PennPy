from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, session, logging, send_from_directory
from passlib.hash import sha256_crypt
import uuid

# Homebuilt imports
from PennPy import db
from PennPy.models import Users
from PennPy.endpoints.products.routes import get_products
from PennPy.endpoints.users.forms import RegistrationForm, LoginForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # Uses WTF to check if POST req and form is valid
    if form.validate_on_submit():
        # Create user object to insert into SQL
        hashed_pass = sha256_crypt.encrypt(str(form.password.data))
        new_user = Users(name=form.name.data, username=form.username.data,
                         email=form.email.data, password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash(f'{form.username.data} already exsists!', 'danger')
            return render_template('register.html', form=form)
        else:
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            # Init session vars
            session['logged_in'] = True
            session['username'] = new_user.username
            session['admin_level'] = 0

            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password_candidate = request.form.get('password')

    # Query for a user with the provided username
    result = Users.query.filter_by(username=username).first()

    # If a user exsists and passwords match - login
    if result != None and sha256_crypt.verify(password_candidate, result.password):

        # Init session vars
        session['logged_in'] = True
        session['username'] = username
        session['admin_level'] = result.admin_level

        flash('Successful Login!', 'success')
        return redirect(url_for('users.dashboard'))

    else:
        flash('Incorrect Login!', 'danger')
        return redirect(url_for('main.index', error="No users found"))


@users.route('/logout')
def logout():
    session.clear()
    flash('Youve logged out!', 'success')
    return redirect(url_for('main.index'))


@users.route('/profile')
def profile():
    if 'username' in session:
        user = Users.query.filter_by(username=session['username']).first()
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('main.index'))


@users.route('/dashboard')
def dashboard():
    # If a session exsists redirect based on admin_level
    if 'username' in session:

        # Pull all users data based off of their username stored in current session
        user = Users.query.filter_by(username=session['username']).first()
        if user.admin_level > 0:
            return render_template("dashboard.html", products=get_products())
        else:
            return render_template("profile.html", user=user)
    else:
        return redirect(url_for('main.index'))


# Check if username or email are already taken
def user_exsists(username, email):
    # Get all Users in SQL
    users = Users.query.all()
    for user in users:
        if username == user.username or email == user.email:
            return True

    # No matching user
    return False
