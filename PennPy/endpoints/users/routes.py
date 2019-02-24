from flask import Blueprint, render_template, flash, request, redirect, url_for, session
from passlib.hash import sha256_crypt

# Homebuilt imports
from PennPy import db
from PennPy.models import User, Address
from PennPy.endpoints.listings.utils import get_listings
from PennPy.endpoints.users.utils import user_exsists, get_addresses

from PennPy.endpoints.listings.forms import CreateListingForm
from PennPy.endpoints.users.forms import RegistrationForm, AddressForm

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
        session['user_id'] = result.id
        print(result)
        print(session['user_id'])

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


@users.route('/account')
def account():
    if 'username' in session:
        user = User.query.filter_by(username=session['username']).first()
        return render_template("account.html", user=user, addresses=get_addresses(user.id))
    else:
        return redirect(url_for('main.index'))


@users.route('/dashboard')
def dashboard():
    # If a session exsists redirect based on admin_level
    if 'username' in session:

        # Pull all users data based off of their username stored in current session
        user = User.query.filter_by(username=session['username']).first()
        if user.admin_level > 0:
            return render_template("dashboard.html", listings=get_listings(), form=CreateListingForm())
        else:
            return redirect(url_for('users.account'))
    else:
        return redirect(url_for('main.index'))


@users.route('/add_address', methods=['POST', 'GET'])
def add_address():

    form = AddressForm()

    # If a session exsists redirect based on admin_level
    if 'username' not in session:
        return redirect(url_for('users.register'))

    # Uses WTF to check if POST req and form is valid
    if form.validate_on_submit():
        new_address = Address(
            name=form.name.data,
            address1=form.address1.data,
            address2=form.address2.data,
            country=form.country.data,
            state=form.state.data,
            city=form.city.data,
            zipcode=form.zipcode.data,
            user_id=session['user_id'])

        # Insert new user into SQL
        db.session.add(new_address)
        db.session.commit()
        return redirect(url_for('users.account'))

    return render_template('add_address.html', form=form)


@users.route('/update_address/<id>', methods=['GET', 'POST'])
def update_address(id):

    # If a session exsists
    if 'username' in session:
        form = AddressForm()
        address = Address.query.get(id)

        # Uses WTF to check if POST req and form is valid
        if form.validate_on_submit():

            address.name = form.name.data
            address.address1 = form.address1.data
            address.address2 = form.address2.data
            address.country = form.country.data
            address.state = form.state.data
            address.city = form.city.data
            address.zipcode = form.zipcode.data

            db.session.commit()
            return redirect(url_for('users.account'))

        else:
            return render_template('update_address.html', form=form, address=address)


# ADD MORE VALIDATION
@users.route('/delete_address/<id>')
def delete_address(id):
    if 'username' in session:
        address = Address.query.get(id)
        db.session.delete(address)
        db.session.commit()
        flash('Address Deleted', 'success')
        return redirect(url_for('users.account'))

    return redirect(url_for('users.register'))
