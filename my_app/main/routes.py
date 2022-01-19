# Done by Muhammad Mustaffa

from flask import Blueprint, redirect, url_for
from flask_login import current_user

from my_app import db
from my_app.models import History

main_bp = Blueprint('main_bp', __name__)


@main_bp.route('/', defaults={'name': 'traveler'})
@main_bp.route('/<name>')
def index(name):
    return redirect('/navigation_dash/')


@main_bp.route('/save/<mean>/<start>/<end>', methods=['GET', 'POST'])
def save_journey(mean, start, end):
    if not current_user.is_anonymous:
        journey = History(mean=mean, start=start, end=end,
                          user_id=current_user.id)
        db.session.add(journey)
        db.session.commit()
    return redirect(url_for('main_bp.index'))
