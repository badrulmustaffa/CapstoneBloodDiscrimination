# Done by Muhammad Mustaffa

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app import db
from my_app.feedback.forms import CommentForm, FeedbackForm, FeedbackReplyForm

from my_app.models import Forum, Feedback, FeedbackReply

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
                                  subject=form.subject.data,
                                  message=form.message.data,
                                  date_posted=datetime.now())
        db.session.add(submitfeedback)
        db.session.commit()
        flash("Feedback submitted, thank you for your help!")
        return redirect(url_for('feedback_bp.post'))

    return render_template('feedback_form.html', form=form)


@feedback_bp.route('/reply', defaults={'name': 'traveler'})
@login_required
def reply(name):
    # reply = FeedbackReply.query.join(Feedback)
    if not current_user.is_anonymous:
        name = current_user.username

    posts = Feedback.query.order_by(Feedback.date_posted.desc()).all()

    return redirect(url_for('feedback_bp.show', post_id=len(posts)))


@feedback_bp.route('/show/<int:post_id>', methods=['GET', 'POST'])
@login_required
def show(post_id):
    if not current_user.is_anonymous:
        name = current_user.username

    posts = Feedback.query.order_by(Feedback.date_posted.desc()).all()
    show = Feedback.query.filter_by(id=post_id).one()
    replies = FeedbackReply.query.filter_by(feedback_id=post_id).order_by(FeedbackReply.date_posted.desc()).all()

    form = FeedbackReplyForm()
    if form.validate_on_submit():
        feedbackreply = FeedbackReply(reply=form.reply.data,
                                      date_posted=datetime.now(),
                                      username=current_user.username,
                                      feedback_id=post_id,
                                      user_id=current_user.id)
        db.session.add(feedbackreply)
        db.session.commit()
        flash("Reply submitted!")
        return redirect(url_for('feedback_bp.show', post_id=post_id))

    return render_template('feedback_show.html', posts=posts, show=show, replies=replies, form=form)
