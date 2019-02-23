import os
import uuid

from PennPy.models import Product
from PennPy.config import Config


def upload_images(images, product_id):

    # Create a target path using product ID
    target = os.path.join(Config.APP_ROOT, 'static/images/products/' + product_id)

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
    target = os.path.join(Config.APP_ROOT, 'static/images/products/' + id)

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
    result = Product.query.filter_by(id=str(uid)).first()

    # If the ID exsists try again with new ID
    if result is not None:
        id_validator(uuid.uuid4())

    return uid
