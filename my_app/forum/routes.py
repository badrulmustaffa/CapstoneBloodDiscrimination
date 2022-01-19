# Done by Muhammad Mustaffa and Manuchimso Opara

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from datetime import datetime

from my_app import db
from my_app.forum.forms import CommentForm

from my_app.models import Forum

forum_bp = Blueprint('forum_bp', __name__, url_prefix='/forum')


@forum_bp.route('/', defaults={'name': 'traveler'})
@login_required
def index(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('index.html',
                           title='Forum page',
                           message='This page is still empty',
                           name=name)


@forum_bp.route('/post', methods=['GET', 'POST'])
def post():
    form = CommentForm()
    if form.validate_on_submit():
        post = Forum(reason=form.reason.data, comment=form.comment.data,
                     date_posted=datetime.now())
        db.session.add(post)
        db.session.commit()
        flash("Comment submitted!")
        return redirect(url_for('forum_bp.post'))
    return render_template('comments_forum.html', form=form)
