from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, logging, send_from_directory

import uuid
import os

# Homebuilt imports
from PennPy import db
from PennPy.config import Config
from PennPy.models import Product
from PennPy.endpoints.products.forms import CreateListingForm


products = Blueprint('products', __name__)


@products.route('/upload', methods=['POST'])
def upload():
    form = CreateListingForm()

    print(form.validate_on_submit())

    if form.validate_on_submit():

        # Make a unique product ID
        product_id = str(id_validator(uuid.uuid4()))

        # Create Product object to insert into SQL
        new_product = Product(id=product_id, name=form.title.data, category=form.category.data, price=form.price.data, description=form.description.data)

        print(new_product)

        # Create a target path for new product image(s) & create director
        target = os.path.join(Config.APP_ROOT, 'static/images/' + product_id)
        os.mkdir(target)

        # Loop through files & save to file system
        for image in request.files.getlist("product_images"):
            print("{} is the file name".format(image.filename))
            filename = image.filename
            destination = "/".join([target, filename])
            image.save(destination)

        # Insert Product into SQL db
        db.session.add(new_product)
        db.session.commit()

        flash('Product Created!', 'success')
        return redirect(url_for('users.dashboard'))
    else:
        return render_template('dashboard.html', form=form)


@products.route('/images/<id>/<filename>')
def get_image(id, filename):
    return send_from_directory('static/images', id + '/' + filename)


@products.route('/image/<id>')
def get_images(id):
    # Create a path with the ID & the root of our App
    target = os.path.join(Config.APP_ROOT, 'static/images/' + id)

    # If path exsists we have images! Return them all
    if os.path.isdir(target):
        return os.listdir(target)

    return False

# remove-->
@products.route('/product/products', methods=['GET'])
def get_products():
    # Get all products in SQL
    products = Product.query.all()

    # Get images for each product
    for product in products:
        images = get_images(product.id)
        product.images = images

    return(products)


@products.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.filter_by(id=id).first()
    if product != None:
        product.images = get_images(product.id)
        return render_template("listing.html", product=product)
    else:
        return redirect(url_for('main.index'))


# Validate the unique ID of our new product to prevent collisions
def id_validator(uid):
    # Query for any product where id matches uid
    result = Product.query.filter_by(id=uid).first()

    # If the ID exsists try again with new ID
    if result != None:
        id_validator(uuid.uuid4())

    return uid
