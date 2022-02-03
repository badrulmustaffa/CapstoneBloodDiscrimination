from flask import Blueprint, render_template, redirect, url_for
from my_app.trial.forms import TrialForm
from datetime import datetime
from my_app import db
from my_app.models import Trial

trial_bp = Blueprint('trial_bp', __name__, url_prefix='/trial')


@trial_bp.route('/tester', methods=['GET', 'POST'])
def tester():
    message = 'Hello world!'
    form = TrialForm()

    if form.validate_on_submit():
        registration = Trial(registration_number=form.registration_id.data,
                             date=datetime.now())

        db.session.add(registration)
        db.session.commit()
        return redirect(url_for('community_bp.view_profile'))

    return render_template('trial_tester.html', fill=message, borang=form)
