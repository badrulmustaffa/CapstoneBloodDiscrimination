from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField, StringField
from wtforms.widgets import TextArea
from wtforms.validators import DataRequired

from my_app import photos


class TesterForm(FlaskForm):
    kit_code = StringField(label='Kit ID', description='Enter here', validators=[DataRequired()])
    blood_image = FileField('Blood Sample', validators=[FileAllowed(photos, 'Images only!'), DataRequired()])
