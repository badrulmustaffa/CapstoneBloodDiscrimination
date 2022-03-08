# Done by Muhammad Mustaffa

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, SelectField, SelectMultipleField, StringField

from my_app import photos


class ProfileForm(FlaskForm):
    """ Class for the profile form """
    bio = TextAreaField(label='Bio', description='Write something about yourself')
    photo = FileField('Profile picture', validators=[FileAllowed(photos, 'Images only!')])
    sex = SelectField('Sex', choices=['Male', 'Female', 'Non-binary'])
    other = StringField('Other health conditions', description='Separate each condition with a comma ","')

