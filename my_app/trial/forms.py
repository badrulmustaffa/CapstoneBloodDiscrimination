from flask_wtf import FlaskForm
from wtforms import TextField
from wtforms.widgets import TextArea


class TrialForm(FlaskForm):
    registration_id = TextField(label='Registration id', widget=TextArea())
