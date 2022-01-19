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
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('index.html',
                           title='Homepage',
                           message='This page is still empty',
                           name=name)

