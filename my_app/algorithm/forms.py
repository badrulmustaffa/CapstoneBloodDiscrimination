from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, SelectField, StringField

from my_app import photos


class ImageSubmitForm(FlaskForm):
    """ Class for the image submit form """
    kit_id = StringField(label="Kit Registration ID")
    blood_image = FileField(label='Blood Test Image', validators=[FileAllowed(photos, 'Images only!')])
