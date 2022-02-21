from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from my_app.algorithm.forms import TesterForm
from my_app.models import Tester
from datetime import datetime

from my_app import db, images

algorithm_bp = Blueprint('algorithm_bp', __name__, url_prefix='/algorithm')


@algorithm_bp.route('/tester', methods=['GET', 'POST'])
@login_required
def submit():
    form = TesterForm()
    if request.method == 'POST' and form.validate_on_submit():

        filename = 'default.png'

        if 'blood_image' in request.files:

            if request.files['blood_image'].filename != '':

                filename = images.save(request.files['blood_image'])

        # result to be changed when algorithm is ready
        registration = Tester(kit_id=form.kit_code.data, blood_image=filename,
                              result=1)
        db.session.add(registration)
        db.session.commit()
        return redirect(url_for('algorithm_bp.submit'))

    return render_template('algorithm_submit.html', entry=form)

# , date_posted=datetime.now()
