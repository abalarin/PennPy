from flask import Blueprint, Flask, render_template, flash, request, redirect, url_for, logging, send_from_directory, session

# Homebuilt imports
from PennPy import db
from PennPy.models import Product, Users

orders = Blueprint('orders', __name__)

@orders.route('/purchase/<id>')
def purchase(id):
    if 'username' in session:
        product = Product.query.get_or_404(id)
        user = Users.query.filter_by(username=session['username']).first()
        print(user)
        return render_template('checkout.html', product=product, user=user)
        # return redirect(url_for('products.get_product', id=id))
    else:
        return redirect(url_for('users.register'))
