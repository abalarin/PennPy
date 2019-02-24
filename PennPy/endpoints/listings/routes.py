from flask import Blueprint, render_template, flash, request, redirect, url_for, send_from_directory, session

import uuid
import os
import shutil

# Homebuilt imports
from PennPy import db
from PennPy.config import Config
from PennPy.models import Listing
from PennPy.endpoints.listings.forms import CreateListingForm, UpdateListingForm

from PennPy.endpoints.listings.utils import upload_images, get_images, id_validator

listings = Blueprint('listings', __name__)


@listings.route('/upload', methods=['POST'])
def upload():
    form = CreateListingForm()

    if form.validate_on_submit():
        # Make a unique listing ID
        listing_id = str(id_validator(uuid.uuid4()))

        # Create Listing object to insert into SQL
        new_listing = Listing(
            id=listing_id,
            name=form.title.data,
            category=form.category.data,
            price=form.price.data,
            description=form.description.data)

        # Upload Images
        upload_images(request.files.getlist("listing_images"), listing_id)

        # Insert Listing into SQL db
        db.session.add(new_listing)
        db.session.commit()

        flash('Listing Created!', 'success')
        return redirect(url_for('users.dashboard'))
    else:
        return render_template('dashboard.html', form=form)


@listings.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    # First authenticate user is logged in and an ADMIN
    if 'username' in session and session['admin_level'] > 0:
        form = UpdateListingForm()
        listing = Listing.query.get_or_404(id)

        if form.validate_on_submit():

            # Get newly added images from req object and upload them to exsisting directory
            upload_images(request.files.getlist("listing_images"), listing.id)

            # Reassign values to update SQL entry
            listing.name = form.title.data
            listing.category = form.category.data
            listing.price = form.price.data
            listing.description = form.description.data
            db.session.commit()

            return redirect(url_for('listings.get_listing', id=listing.id))

        elif request.method == 'GET':
            listing.images = get_images(listing.id)
            form.description.data = listing.description
            return render_template("update_listing.html", listing=listing, form=form)

    return redirect(url_for('main.index'))


@listings.route('/delete/<id>')
def delete_listing(id):
    if session['admin_level'] > 0:
        listing = Listing.query.get(id)

        target = os.path.join(Config.APP_ROOT, 'static/images/listings/' + id)

        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)

        db.session.delete(listing)
        db.session.commit()

        flash('Your listing has been deleted!', 'success')
        return redirect(url_for('users.dashboard'))


@listings.route('/delete/<id>/<filename>')
def delete_image(id, filename):
    if session['admin_level'] > 0:
        target = os.path.join(
            Config.APP_ROOT, 'static/images/listings/' + id + "/" + filename)
        os.remove(target)

        return redirect(url_for("listings.update", id=id))


@listings.route('/images/<id>/<filename>')
def get_image(id, filename):
    return send_from_directory('static/images/listings/', id + '/' + filename)


@listings.route('/listing/<id>', methods=['GET'])
def get_listing(id):
    listing = Listing.query.get_or_404(id)
    listing.images = get_images(listing.id)

    return render_template("listing.html", listing=listing)
