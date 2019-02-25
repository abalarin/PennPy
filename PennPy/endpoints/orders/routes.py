from flask import Blueprint, render_template, redirect, url_for, session, request, flash
import paypalrestsdk

# Homebuilt imports
from PennPy.endpoints.listings.utils import get_images
from PennPy.models import Listing, User


orders = Blueprint('orders', __name__)


@orders.route('/cart/<id>')
def cart(id):
    if 'username' in session:
        listing = Listing.query.get_or_404(id)
        user = User.query.filter_by(username=session['username']).first()
        return render_template('review_order.html', listing=listing, user=user, images=get_images(id))
    else:
        return redirect(url_for('users.register'))


@orders.route('/paypal_checkout/<id>')
def paypal_checkout(id):

    listing = Listing.query.get_or_404(id)

    payment = paypalrestsdk.Payment({
        "intent": "sale",
        "payer": {
            "payment_method": "paypal"},
        "redirect_urls": {
            "return_url": "http://pennpy.com/paypal_review",
            "cancel_url": "http://pennpy.com/"},
        "transactions": [{
            "item_list": {
                "items": [{
                    "name": listing.name,
                    "sku": listing.category,
                    "price": listing.price,
                    "currency": "USD",
                    "quantity": 1}]},
            "amount": {
                "total": listing.price,
                "currency": "USD"},
            "description": listing.description}]})

    if payment.create():
        print("Payment created successfully")
    else:
        print(payment.error)

    for link in payment.links:
        if link.rel == "approval_url":
            approval_url = link.href
            # print("Redirect for approval: %s" % (approval_url))

    return redirect(approval_url)


@orders.route('/paypal_review')
def paypal_review():
    payment = paypalrestsdk.Payment.find(request.args.get('paymentId'))
    address = payment.payer.payer_info.shipping_address
    order_summary = payment.transactions[0]

    return render_template('place_order.html', address=address, order=order_summary, payment=payment)


@orders.route('/paypal_pay')
def paypal_pay():

    payment_id = request.args.get('paymentId')
    payer_id = request.args.get('PayerID')
    payment = paypalrestsdk.Payment.find(payment_id)

    if payment.execute({"payer_id": str(payer_id)}):
        print("Payment execute successfully")
    else:
        print(payment.error)  # Error Hash

    flash("You've bought this item!", 'success')
    return redirect(url_for('users.account'))
