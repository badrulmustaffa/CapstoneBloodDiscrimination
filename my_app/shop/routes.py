import sqlite3, random, string

from flask import Blueprint, render_template, request, session, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app.shop.forms import ShoppingCartForm
from my_app import db
from my_app.models import ShoppingCart, Tester

shop_bp = Blueprint('shop_bp', __name__, url_prefix='/shop')


@shop_bp.route('/product', methods=['GET', 'POST'])
@login_required
# @login_required
def product():
    if not current_user.is_anonymous:
        name = current_user.username

    form = ShoppingCartForm()
    # cart = ShoppingCart.query.filter_by(username=name).first()
    cart = session.get('cart', {'kit': 0, 'machine': 0})

    if request.method == 'POST':
        item = request.form.get('itemid')
        cart[item] += 1
        flash('Your shopping cart has been updated!')
        session['cart'] = cart

    return render_template('shop_product.html', form=form, name=name, cart=cart)


@shop_bp.route('/payment', defaults={'name': 'traveler'}, methods=['GET', 'POST'])
@login_required
def payment(name):
    if not current_user.is_anonymous:
        name = current_user.username

    if session.get('cart', None) is not None:
        cart = session.get('cart')
        session['cart'] = cart
        kitqty = session['cart']['kit']
        machqty = session['cart']['machine']
        kitprice = round(kitqty * 9.85, 2)
        machprice = machqty * 100
        totalprice = round((machprice + kitprice), 2)
        tax = round(0.2 * totalprice, 2)

    return render_template('shop_payment.html',
                           name=name,
                           cart=cart,
                           kitprice=kitprice,
                           machprice=machprice,
                           totalprice=totalprice,
                           tax=tax)


@shop_bp.route('/clear')
@login_required
def clear():
    session.pop('cart', default=None)
    flash('Shopping cart emptied!')
    return redirect("/shop/product")


@shop_bp.route('/checkout', defaults={'name': 'traveler'})
@login_required
def checkout(name):
    if not current_user.is_anonymous:
        name = current_user.username

    if session.get('cart', None) is not None:
        cart = session.get('cart')
        session['cart'] = cart
        kitqty = session['cart']['kit']
        machqty = session['cart']['machine']
        kitamount = kitqty
        ID = 0
        refnum = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) \
                 + '-' \
                 + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))

        while ID < kitamount:
            kit_ID = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            ID = ID + 1

            registerID = Tester(username=name,
                                kit_id=kit_ID,
                                ref_num=refnum,
                                blood_image='Pending',
                                result='-', date_posted='-'
                                )
            db.session.add(registerID)
            db.session.commit()

        purchase = ShoppingCart(username=name,
                                ref_num=refnum,
                                QuantityA=kitqty,
                                QuantityB=machqty,
                                date_purchased=datetime.now())

        db.session.add(purchase)
        db.session.commit()

        session.pop('cart', default=None)

    flash('Purchase confirmed!')
    # return redirect(url_for('shop_bp.confirm', refnum=refnum))
    return render_template('shop_confirm.html', refnum=refnum)


@shop_bp.route('/gen_kitid')
@login_required
def gen_kitid():
    # function to generate kid ID
    result_str = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4)) \
                 + '-' \
                 + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return redirect(url_for('shop_bp.product', result_str=result_str))


@shop_bp.route('/confirm')
@login_required
def confirm():
    # refnum = session.get('refnum')
    # reference = ShoppingCart.query.filter_by(ref_num=refnum).all()
    return render_template('shop_confirm.html', reference=reference)
