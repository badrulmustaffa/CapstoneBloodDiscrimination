from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class TrialForm(FlaskForm):
    registration_id = TextAreaField(label='Registration id', widget=TextArea())
