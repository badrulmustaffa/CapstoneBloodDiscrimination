# Done by Muhammad Mustaffa

from datetime import timedelta
from sqlite3 import IntegrityError
from urllib.parse import urlparse, urljoin

from flask import Blueprint, render_template, flash, redirect, url_for, request, abort
from flask_login import login_user, login_required, logout_user

from my_app import db, login_manager
from my_app.auth.forms import SignupForm, LoginForm
from my_app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, type=form.type.data)
        user.set_password(form.password.data)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"Hello, {user.username}! You are signed up.")
        except IntegrityError:
            db.session.rollback()
            flash(f"Error, unable to register {form.email.data}.", 'error')
            return redirect(url_for("auth.signup"))

        login_user(user, remember=True, duration=timedelta(minutes=1))
        flash("You are logged in!")
        return redirect(url_for('community_bp.profile', name=user.username))

    return render_template('auth_signup.html',
                           title='Sign Up',
                           form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        login_user(user, remember=form.remember.data, duration=timedelta(minutes=1))
        next = request.args.get('next')

        if not is_safe_url(next):
            return abort(400)

        flash("You are logged in!")
        return redirect(next or url_for('community_bp.profile', name=user.username))
    return render_template('auth_login.html', title='Login', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_bp.index'))


@login_manager.user_loader
def load_user(user_id):
    """ Takes a user ID and returns a user object or None if the user does not exist"""
    if user_id is not None:
        return User.query.get(user_id)
    return None


def is_safe_url(target):
    host_url = urlparse(request.host_url)
    redirect_url = urlparse(urljoin(request.host_url, target))
    return redirect_url.scheme in ('http', 'https') and host_url.netloc == redirect_url.netloc


def get_safe_redirect():
    url = request.args.get('next')
    if url and is_safe_url(url):
        return url

    url = request.referrer
    if url and is_safe_url(url):
        return url
    return '/'


@login_manager.unauthorized_handler
def unauthorized():
    """Redirect unauthorized users to Login page."""
    flash('You must be logged in to view that page.')
    return redirect(url_for('auth.login'))
