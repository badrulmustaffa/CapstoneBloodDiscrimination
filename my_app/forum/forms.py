# Done by Muhammad Mustaffa and Manuchimso Opara

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, SelectField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class CommentForm(FlaskForm):
    reason = SelectField(choices=['Question', 'Complaint'], validators=[DataRequired()])
    comment = TextField('Comment', widget=TextArea(), validators=[DataRequired()])
