from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from my_app import db, photos

algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')


@algorithm_bp.route('/submit', defaults={'name': 'traveler'})
@login_required
def submit(name):
    if not current_user.is_anonymous:
        name = current_user.username

    return render_template('algorithm_submit.html')