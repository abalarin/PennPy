from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, logging, send_from_directory

import uuid, os

# Homebuilt imports
from PennPy import mysql
from PennPy.models import Product
from PennPy.config import Config


products =  Blueprint('products', __name__)

@products.route('/upload', methods=['POST'])
def upload():
    # Create SQL Product Object
    product_id = str(id_validator(uuid.uuid4()))
    product_name = request.form.get('product_name')
    product_category = request.form.get('product_category')
    product_price = request.form.get('product_cost')
    product_description = request.form.get('product_description')
    image_root = "images/" + product_id + "/"

    # Create a target path for new product image(s)
    target = os.path.join(Config.APP_ROOT, 'static/images/' + product_id)

    # If not directory exsists create new one
    if not os.path.isdir(target):
        os.mkdir(target)

    # Loop through files & save to file system
    for file in request.files.getlist("product_images"):
        print("{} is the file name".format(file.filename))
        filename = file.filename
        destination = "/".join([target, filename])
        file.save(destination)

    # Create SQL Connection & INSERT our new product
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO product(name, category, price, description, image_root, id) VALUES(%s, %s, %s, %s, %s, %s)", (product_name, product_category, product_price, product_description, image_root, product_id))
    mysql.connection.commit()
    cur.close()

    flash('Image Uploaded!', 'success')
    return redirect(url_for('users.dashboard'))

@products.route('/images/<id>/<filename>')
def get_image(id, filename):
    return send_from_directory('static/images', id +'/' + filename)

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
