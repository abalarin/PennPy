import os
import uuid

from PennPy.models import Listing
from PennPy.config import Config


def upload_images(images, listing_id):

    # Create a target path using listing ID
    target = os.path.join(Config.APP_ROOT, 'static/images/listings/' + listing_id)

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
    target = os.path.join(Config.APP_ROOT, 'static/images/listings/' + id)

    # If path exsists we have images! Return them all
    if os.path.isdir(target):
        return os.listdir(target)

    return False


def get_listings():
    # Get all listings in SQL
    listings = Listing.query.all()

    # Get images for each listing
    for listing in listings:
        images = get_images(listing.id)
        listing.images = images

    return(listings)


# Validate the unique ID of our new listing to prevent collisions
def id_validator(uid):
    # Query for any listing where id matches uid
    result = Listing.query.filter_by(id=str(uid)).first()

    # If the ID exsists try again with new ID
    if result is not None:
        id_validator(uuid.uuid4())

    return uid
