from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from my_app.algorithm.forms import TesterForm
from my_app.models import Tester

from my_app import db, photos

algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')


@algorithm_bp.route('/tester', defaults={'name': 'traveler'})
@login_required
def submit(name):
    form = TesterForm()
    if form.validate_on_submit():
        registration = Tester(kit_id=form.kit_code.data)

        db.session.add(registration)
        db.session.commit()
        return redirect(url_for('algorithm_bp.tester'))

    return render_template('algorithm_submit.html', entry=form)
