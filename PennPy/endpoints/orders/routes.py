from flask import Blueprint, render_template, redirect, url_for, session

# Homebuilt imports
from PennPy.models import Products, Users

orders = Blueprint('orders', __name__)


@orders.route('/purchase/<id>')
def purchase(id):
    if 'username' in session:
        product = Products.query.get_or_404(id)
        user = Users.query.filter_by(username=session['username']).first()
        print(user)
        return render_template('checkout.html', product=product, user=user)
        # return redirect(url_for('products.get_product', id=id))
    else:
        return redirect(url_for('users.register'))
