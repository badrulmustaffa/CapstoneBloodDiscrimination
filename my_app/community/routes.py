# Done by Muhammad Mustaffa

from flask import Blueprint, render_template, redirect, url_for, request, flash, send_from_directory
from flask_login import login_required, current_user
from pathlib import Path
from datetime import datetime
import my_app.config
from my_app import db, photos
from my_app.community.forms import ProfileForm
from my_app.models import Profile, User, History, ShoppingCart, Tester
from my_app.config import Config

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
    choices = ['High Blood Pressure', 'History of Heart Attack',
               'Coronary Artery Disease',
               'Undiagnosed Chest Pain', 'Shortness of Breath', 'Irregular Heartbeart',
               'Artificial Heart Valve', 'Peripheral Vascular Disease',
               'Congestive Heart Failure',
               'Diabetes', 'Kidney Disease', 'Cancer', 'Epilepsy/Seizure',
               'Mental Illness',
               'Emphysema', 'Asthma', 'Chronic Cough', 'Heart Murmur', 'Wheezing',
               'Stroke', 'High Cholestrol',
               'Thyroid Disease', 'Seasonal Allergies', 'Bleeding/Clotting Disorder',
               'Varicose Veins',
               'Gastrointestinal Disease', 'Liver Disease/Hepatitis', 'HIV',
               'History of Covid']

    if request.method == 'POST' and form.validate_on_submit():
        # Set photo name to default if no photos attached
        filename = 'default.png'
        # CHeck if form contains photo
        if 'photo' in request.files:
            # if the filename is not empty, save the the photo
            if request.files['photo'].filename != '':
                # Save to photos in my_app
                filename = photos.save(request.files['photo'])

        conditions = ', '.join([str(item) for item in request.form.getlist('check')])

        if form.other.data:
            conditions += ", " + form.other.data

        bio = form.bio.data
        if not form.bio.data:
            bio = 'No bio yet'

        # Create a profile for database
        profile = Profile(photo=filename, bio=bio, sex=form.sex.data,
                          username=current_user.username, date=datetime.now(),
                          user_id=current_user.id, conditions=conditions)
        db.session.add(profile)
        db.session.commit()
        return redirect(
            url_for('community_bp.view_profile', username=profile.username))

    return render_template('profile_create.html', form=form, choices=choices,
                           username=current_user.username)


@community_bp.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    choices = ['High Blood Pressure', 'History of Heart Attack',
               'Coronary Artery Disease',
               'Undiagnosed Chest Pain', 'Shortness of Breath', 'Irregular Heartbeart',
               'Artificial Heart Valve', 'Peripheral Vascular Disease',
               'Congestive Heart Failure',
               'Diabetes', 'Kidney Disease', 'Cancer', 'Epilepsy/Seizure',
               'Mental Illness',
               'Emphysema', 'Asthma', 'Chronic Cough', 'Heart Murmur', 'Wheezing',
               'Stroke', 'High Cholestrol',
               'Thyroid Disease', 'Seasonal Allergies', 'Bleeding/Clotting Disorder',
               'Varicose Veins',
               'Gastrointestinal Disease', 'Liver Disease/Hepatitis', 'HIV',
               'History of Covid']
    profile = Profile.query.join(User).filter_by(id=current_user.id).first()
    form = ProfileForm(obj=profile)  # Prepopulate
    if request.method == 'POST' and form.validate_on_submit():
        filename = profile.photo
        if 'photo' in request.files:
            if request.files['photo'].filename != '':
                # Update the saved photos in my_app
                filename = photos.save(request.files['photo'])

        conditions = ', '.join([str(item) for item in request.form.getlist('check')])
        if form.other.data:
            conditions += ", " + form.other.data

        # Update other detail
        profile.bio = form.bio.data
        profile.photo = filename
        profile.sex = form.sex.data
        profile.conditions = conditions
        profile.date = datetime.now()
        db.session.commit()

        flash('Profile updated!')
        return redirect(url_for('community_bp.view_profile', username=profile.username))
    return render_template('profile_create.html', form=form, username=profile.username,
                           choices=choices)


@community_bp.route('/view_profile', methods=['GET', 'POST'])
@community_bp.route('/view_profile/<username>', methods=['POST', 'GET'])
@login_required
def view_profile(username=None):
    if username is None:
        username = current_user.username

    type = current_user.type
    profile = Profile.query.filter_by(username=username).one()
    history = History.query.filter_by(user_id=current_user.id).all()
    purchases = ShoppingCart.query.filter_by(username=current_user.username).all()
    kit_id = Tester.query.filter_by(username=current_user.username).all()

    return render_template('profile_view.html', profile=profile, usertype=type, history=history, purchases=purchases,
                           kit_id=kit_id)


@community_bp.route('/profile_picture/<filename>')
def profile_picture(filename):
    return send_from_directory(Config.UPLOADED_PHOTOS_DEST, '/user', filename=filename, as_attachment=True)


@community_bp.route('/blood_image/<filename>')
def blood_image(filename):
    return send_from_directory(Config.UPLOADED_IMAGES_DEST, '/database', filename=filename, as_attachment=True)
