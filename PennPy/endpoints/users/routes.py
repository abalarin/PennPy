from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from passlib.hash import sha256_crypt

# Homebuilt imports
from PennPy import db
from PennPy.models import User
from PennPy.endpoints.products.utils import get_products
from PennPy.endpoints.users.utils import user_exsists

from PennPy.endpoints.products.forms import CreateListingForm
from PennPy.endpoints.users.forms import RegistrationForm

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    # Uses WTF to check if POST req and form is valid
    if form.validate_on_submit():
        # Create user object to insert into SQL
        hashed_pass = sha256_crypt.encrypt(str(form.password.data))
        new_user = User(
            name=form.name.data,
            username=form.username.data,
            email=form.email.data,
            password=hashed_pass)

        if user_exsists(new_user.username, new_user.email):
            flash('User already exsists!', 'danger')
            return render_template('register.html', form=form)
        else:
            # Insert new user into SQL
            db.session.add(new_user)
            db.session.commit()

            # Init session vars
            session['logged_in'] = True
            session['username'] = new_user.username
            session['admin_level'] = 0

            flash('Account created!', 'success')
            return redirect(url_for('main.index'))

    return render_template('register.html', form=form)


@users.route('/login', methods=['POST'])
def login():

    username = request.form.get('username')
    password_candidate = request.form.get('password')

    # Query for a user with the provided username
    result = User.query.filter_by(username=username).first()

    # If a user exsists and passwords match - login
    if result is not None and sha256_crypt.verify(password_candidate, result.password):

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
        user = User.query.filter_by(username=session['username']).first()
        return render_template("profile.html", user=user)
    else:
        return redirect(url_for('main.index'))


@users.route('/dashboard')
def dashboard():
    # If a session exsists redirect based on admin_level
    if 'username' in session:

        # Pull all users data based off of their username stored in current session
        user = User.query.filter_by(username=session['username']).first()
        if user.admin_level > 0:
            return render_template("dashboard.html", products=get_products(), form=CreateListingForm())
        else:
            return render_template("profile.html", user=user)
    else:
        return redirect(url_for('main.index'))
