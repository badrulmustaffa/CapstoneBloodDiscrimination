# Done by Muhammad Mustaffa

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user

from my_app import db, photos
from my_app.community.forms import ProfileForm
from my_app.models import Profile, User, History

community_bp = Blueprint('community_bp', __name__, url_prefix='/community')


@community_bp.route('/', defaults={'name': 'traveler'})
@login_required
def index(name):
    if not current_user.is_anonymous:
        name = current_user.username
    return render_template('index.html',
                           title='Community page',
                           message='This page is still empty',
                           name=name)


@community_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = Profile.query.join(User).filter(User.id == current_user.id).first()
    if profile:
        return redirect(url_for('community_bp.view_profile',
                                username=current_user.username))
    else:
        flash("No profile found. Please create a new one")
        return redirect((url_for('community_bp.create_profile')))


@community_bp.route('/create_profile', methods=['GET', 'POST'])
@login_required
def create_profile():
    form = ProfileForm()
    if request.method == 'POST' and form.validate_on_submit():
        # Set photo name to default if no photos attached
        filename = 'default.jpg'
        # CHeck if form contains photo
        if 'photo' in request.files:
            # if the filename is not empty, save the the photo
            if request.files['photo'].filename != '':
                # Save to photos in my_app
                filename = photos.save(request.files['photo'])

        # Create a profile for database
        profile = Profile(photo=filename, bio=form.bio.data,
                          username=current_user.username,
                          user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()
        return redirect(
            url_for('community_bp.view_profile', username=profile.username))
    return render_template('profile.html', form=form,
                           username=current_user.username,
                           message='New profile')


@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    # profile = Profile.Query
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)  # Prepopulate
    if request.method == 'POST' and form.validate_on_submit():
        filename = profile.photo
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                # Update the saved photos in my_app
                filename = photos.save(request.files['photo'])

        # Update other detail
        profile.bio = form.bio.data
        profile.photo = filename
        db.session.commit()
        return redirect(url_for('community_bp.view_profile', username=profile.username))
    return render_template('profile.html', form=form, username=profile.username,
                           message='Profile update')


@community_bp.route('/display_profiles', methods=['GET', 'POST'])
@community_bp.route('/display_profiles/<username>', methods=['POST', 'GET'])
@login_required
def display_profiles(username=None):
    results = None
    if username is None:
        if request.method == 'POST':
            term = request.form['search_term']
            if term == "":
                flash("Enter a name to search for")
                return redirect(url_for('community_bp.index'))
            results = Profile.query.filter(Profile.username.contains(term)).all()
    else:
        term = username
        results = Profile.query.filter(Profile.username.contains(term)).all()
    if not results:
        flash("Username not found")
        return redirect(url_for('community_bp.index'))

    urls = []
    for result in results:
        if result.photo:
            url = photos.url(result.photo)
            urls.append(url)
    return render_template('profile_display.html', profiles=zip(results, urls))


@community_bp.route('/view_profile', methods=['GET', 'POST'])
@community_bp.route('/view_profile/<username>', methods=['POST', 'GET'])
@login_required
def view_profile(username=None):
    if username is None:
        username = current_user.username

    results = Profile.query.filter_by(username=username).all()
    history = History.query.filter_by(user_id=current_user.id).all()
    urls = []
    for result in results:
        if result.photo:
            url = photos.url(result.photo)
            urls.append(url)
    return render_template('profile_view.html', profiles=zip(results, urls), history=history)


