# Done by Muhammad Mustaffa

from flask import Blueprint, redirect, url_for, render_template
from flask_login import login_required, current_user

from my_app import db
from my_app.models import History

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', defaults={'name': 'traveler'})
@main_bp.route('/<name>')
@login_required
def index(name):
    return redirect(url_for('main_bp.dashboard'))


@main_bp.route('/dashboard')
@login_required
def dashboard():
    if not current_user.is_anonymous:
        name = current_user.username

    return render_template('main_dashboard.html')


@main_bp.route('/about')
def about():
    return render_template('blog_about.html')


@main_bp.route('/FAQ')
def faq():
    return render_template('blog_faq.html')


@main_bp.route('/credit')
def credit():
    return render_template('blog_credits.html')

