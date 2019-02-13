from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, logging, send_from_directory

import uuid
import os

# Homebuilt imports
from PennPy import mysql
from PennPy import db
from PennPy.config import Config
from PennPy.models import Product


products = Blueprint('products', __name__)


@products.route('/upload', methods=['POST'])
def upload():
    # Create SQL Product Object - Could be condensed into is own func?
    product_id = str(id_validator(uuid.uuid4()))
    product_name = request.form.get('product_name')
    product_category = request.form.get('product_category')
    product_price = request.form.get('product_cost')
    product_description = request.form.get('product_description')
    image_root = "images/" + product_id + "/"

    # Create Product object to insert into SQL
    new_product = Product(id=product_id, name=product_name, category=product_category,
                          price=product_price, description=product_description, image_root=image_root)

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


@products.route('/product/products', methods=['GET'])
def get_products():
    # Create SQL Connection & Fetch all products
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM product")
    products = cur.fetchall()
    cur.close()

    # Get images for each product
    for product in products:
        images = get_images(product["id"])
        product['images'] = images

    return(products)


# Validate the unique ID of our new product & prevent collisions
def id_validator(uid):
    cur = mysql.connection.cursor()
    result = cur.execute("SELECT * FROM product WHERE id = %s", [uid])
    cur.close()

    # If the ID exsists try again with new ID
    if result > 0:
        id_validator(uuid.uuid4())

    return uid
