from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app import db
from my_app.feedback.forms import CommentForm, FeedbackForm

from my_app.models import Forum, Feedback

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
