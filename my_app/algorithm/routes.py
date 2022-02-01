from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from my_app import db, photos
from my_app.algorithm.forms import ImageSubmitForm
from my_app.community.forms import ProfileForm
from my_app.models import Profile, User, History

algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')


@algorithm_bp.route('/submit', defaults={'name': 'traveler'})
@login_required
def submit(name):
    form = ImageSubmitForm
    if not current_user.is_anonymous:
        name = current_user.username

    return render_template('algorithm_submit.html',
                           title='Submit Blood Image',
                           form=form,
                           name=name)


@algorithm_bp.route('/result', defaults={'name': 'traveler'})
@login_required
def result(name):
    if not current_user.is_anonymous:
        name = current_user.username

    return render_template('index.html',
                           title='Blood Result',
                           message='This page is still empty',
                           message2='Hi Jack',
                           name=name)
