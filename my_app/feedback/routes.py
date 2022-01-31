# Done by Muhammad Mustaffa and Manuchimso Opara

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app import db
from my_app.feedback.forms import CommentForm, FeedbackForm

from my_app.models import Forum, Feedback

feedback_bp = Blueprint('feedback_bp', __name__, url_prefix='/feedback')


@feedback_bp.route('/', defaults={'name': 'traveler'})
@login_required
def index(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('index.html',
                           title='Forum page',
                           message='This page is still empty',
                           name=name)


@feedback_bp.route('/post', methods=['GET', 'POST'])
def post():
    form = FeedbackForm()
    if form.validate_on_submit():
        submitfeedback = Feedback(name=form.name.data, email=form.email.data,
                                  subject=form.subject.data, message=form.message.data,
                                  date_posted=datetime.now())
        db.session.add(submitfeedback)
        db.session.commit()
        flash("Comment submitted!")
        return redirect(url_for('feedback_bp.post'))
    return render_template('forum_comments.html', form=form)
