from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, logging, send_from_directory, session, escape

import uuid
import os
import shutil

# Homebuilt imports
from PennPy import db
from PennPy.config import Config
from PennPy.models import Product
from PennPy.endpoints.products.forms import CreateListingForm, UpdateListingForm


products = Blueprint('products', __name__)


@products.route('/upload', methods=['POST'])
def upload():
    form = CreateListingForm()

    if form.validate_on_submit():
        # Make a unique product ID
        product_id = str(id_validator(uuid.uuid4()))

        # Create Product object to insert into SQL
        new_product = Product(id=product_id, name=form.title.data, category=form.category.data,
                              price=form.price.data, description=form.description.data)

        # Upload Images
        upload_images(request.files.getlist("product_images"), product_id)

        # Insert Product into SQL db
        db.session.add(new_product)
        db.session.commit()

        flash('Product Created!', 'success')
        return redirect(url_for('users.dashboard'))
    else:
        return render_template('dashboard.html', form=form)


@products.route('/update/<id>', methods=['GET', 'POST'])
def update(id):

    # First authenticate user is logged in and an ADMIN
    if 'username' in session and session['admin_level'] > 0:
        form = UpdateListingForm()
        product = Product.query.get_or_404(id)

        if form.validate_on_submit():

            # Get newly added images from req object and upload them to exsisting directory
            upload_images(request.files.getlist("product_images"), product.id)

            # Reassign values to update SQL entry
            product.name = form.title.data
            product.category = form.category.data
            product.price = form.price.data
            product.description = form.description.data
            db.session.commit()

            return redirect(url_for('products.get_product', id=product.id))

        elif request.method == 'GET':
            product.images = get_images(product.id)
            form.description.data = product.description
            return render_template("admin_listing.html", product=product, form=form)


@products.route('/delete/<id>')
def delete_listing(id):
    if session['admin_level'] > 0:
        product = Product.query.get(id)

        target = os.path.join(Config.APP_ROOT, 'static/images/' + id)

        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)

        db.session.delete(product)
        db.session.commit()

        flash('Your listing has been deleted!', 'success')
        return redirect(url_for('users.dashboard'))


@products.route('/images/<id>/<filename>')
def get_image(id, filename):
    return send_from_directory('static/images', id + '/' + filename)


@products.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    product.images = get_images(product.id)

    return render_template("listing.html", product=product)


# ------------ MOVE Out of routes-------------------


def upload_images(images, product_id):

    # Create a target path using product ID
    target = os.path.join(Config.APP_ROOT, 'static/images/' + product_id)

    # If target director exsist then this is just an update, no need to create new dir
    if not os.path.isdir(target):
        os.mkdir(target)

    # Loop through all images and upload
    for image in images:
        filename = image.filename
        destination = "/".join([target, filename])
        image.save(destination)


def get_images(id):
    # Create a path with the ID & the root of our App
    target = os.path.join(Config.APP_ROOT, 'static/images/' + id)

    # If path exsists we have images! Return them all
    if os.path.isdir(target):
        return os.listdir(target)

    return False


def get_products():
    # Get all products in SQL
    products = Product.query.all()

    # Get images for each product
    for product in products:
        images = get_images(product.id)
        product.images = images

    return(products)


# Validate the unique ID of our new product to prevent collisions
def id_validator(uid):
    # Query for any product where id matches uid
    result = Product.query.filter_by(id=uid).first()

    # If the ID exsists try again with new ID
    if result != None:
        id_validator(uuid.uuid4())

    return uid

# ------------ MOVE Out of routes-------------------
