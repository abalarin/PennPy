from flask import Blueprint, render_template, flash, request, redirect, url_for, send_from_directory, session

import uuid
import os
import shutil

# Homebuilt imports
from PennPy import db
from PennPy.config import Config
from PennPy.models import Product
from PennPy.endpoints.products.forms import CreateListingForm, UpdateListingForm

from PennPy.endpoints.products.utils import upload_images, get_images, id_validator

products = Blueprint('products', __name__)

# POST
@products.route('/upload', methods=['POST'])
def upload():
    form = CreateListingForm()

    if form.validate_on_submit():
        # Make a unique product ID
        product_id = str(id_validator(uuid.uuid4()))

        # Create Product object to insert into SQL
        new_product = Product(
            id=product_id,
            name=form.title.data,
            category=form.category.data,
            price=form.price.data,
            description=form.description.data)

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

    return redirect(url_for('main.index'))


@products.route('/delete/<id>')
def delete_listing(id):
    if session['admin_level'] > 0:
        product = Product.query.get(id)

        target = os.path.join(Config.APP_ROOT, 'static/images/products/' + id)

        if os.path.isdir(target):
            shutil.rmtree(target, ignore_errors=True)

        db.session.delete(product)
        db.session.commit()

        flash('Your listing has been deleted!', 'success')
        return redirect(url_for('users.dashboard'))


@products.route('/delete/<id>/<filename>')
def delete_image(id, filename):
    if session['admin_level'] > 0:
        target = os.path.join(
            Config.APP_ROOT, 'static/images/products/' + id + "/" + filename)
        os.remove(target)

        return redirect(url_for("products.update", id=id))


@products.route('/images/<id>/<filename>')
def get_image(id, filename):
    return send_from_directory('static/images/products/', id + '/' + filename)


@products.route('/product/<id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    product.images = get_images(product.id)

    return render_template("listing.html", product=product)
