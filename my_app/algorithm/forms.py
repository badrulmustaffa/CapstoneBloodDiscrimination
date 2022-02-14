from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from wtforms import TextAreaField, FileField
from wtforms.widgets import TextArea

from my_app import photos


class TesterForm(FlaskForm):
    kit_code = TextAreaField(label='Kit ID', description='Enter here', widget=TextArea())
