from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app import db
from my_app.shop.forms import ShoppingCartForm

from my_app.models import ShoppingCart

shop_bp = Blueprint('shop_bp', __name__, url_prefix='/shop')


@shop_bp.route('/product', defaults={'name': 'traveler'})
# @login_required
def product(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('shop_product.html', name=name)


@shop_bp.route('/payment', defaults={'name': 'traveler'})
# @login_required
def payment(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('shop_payment.html', name=name)


@shop_bp.route('/addcart', methods=['GET', 'POST'])
def add_product_to_cart():
    form = ShoppingCartForm()
    if not current_user.is_anonymous:
        name = current_user.username

    if request.method == 'POST' and form.validate():
        addtocart = ShoppingCart(username=name, QuantityA=form.QuantityA.data, QuantityB=form.QuantityB.data)

        db.session.add(addtocart)
        db.session.commit()
        flash('Item added to your Shopping Cart!')
        return redirect(url_for('shop_bp.product'))

    return redirect(url_for('shop_bp.product'))
