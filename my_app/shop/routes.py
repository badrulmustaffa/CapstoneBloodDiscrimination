import sqlite3, random, string

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app.shop.forms import ShoppingCartForm
from my_app import db
from my_app.models import ShoppingCart

shop_bp = Blueprint('shop_bp', __name__, url_prefix='/shop')


@shop_bp.route('/product', methods=['GET', 'POST'])
# @login_required
def product():
    if not current_user.is_anonymous:
        name = current_user.username

    form = ShoppingCartForm()
    # cart = ShoppingCart.query.filter_by(username=name).first()
    cart = session.get('cart', {'kit': 0, 'machine': 0})

    if request.method =='POST':
        item = request.form.get('itemid')
        cart[item] += 1
        flash('Your shopping cart has been updated!')
        session['cart'] = cart

    return render_template('shop_product.html', form=form, name=name, cart=cart)

    # if request.method == 'POST' and form.validate():
    #     session['item'] = request.form['itemA']
    #     session['item'] = request.form['itemB']
        # if cart:
        #     # cart.QuantityA = form.QuantityA.data
        #     # cart.QuantityB = form.QuantityB.data
        #     # db.session.commit()
        #     # flash('Updated your Shopping Cart!')
        #

        # else:
        #     addtocart = ShoppingCart(username=name, QuantityA=form.QuantityA.data, QuantityB=form.QuantityB.data)
        #     db.session.add(addtocart)
        #     db.session.commit()
        #     flash('Item added to your Shopping Cart!')
        #     return redirect(url_for('shop_bp.product'))




@shop_bp.route('/payment', defaults={'name': 'traveler'}, methods=['GET', 'POST'])
# @login_required
def payment(name):

    if not current_user.is_anonymous:
        name = current_user.username

    if session.get('cart', None) is not None:
        cart = session.get('cart')
        session['cart'] = cart
        kitqty = session['cart']['kit']
        machqty = session['cart']['machine']
        kitprice = kitqty*5
        machprice = machqty*100
        totalprice = machprice + kitprice

    return render_template('shop_payment.html', name=name, cart=cart, kitprice=kitprice, machprice=machprice, totalprice=totalprice)


@shop_bp.route('/clear')
def clear():
    session.pop('cart', default=None)
    flash('Shopping cart emptied!')
    return redirect("/shop/product")

@shop_bp.route('/checkout', defaults={'name': 'traveler'})
def checkout(name):
    if not current_user.is_anonymous:
        name = current_user.username

    if session.get('cart', None) is not None:
        cart = session.get('cart')
        session['cart'] = cart
        kitqty = session['cart']['kit']
        machqty = session['cart']['machine']

        purchase = ShoppingCart(username=name, QuantityA=kitqty, QuantityB=machqty)
        db.session.add(purchase)
        db.session.commit()

        session.pop('cart', default=None)

    flash('purchase confirmed!')
    return redirect(url_for('shop_bp.product'))
