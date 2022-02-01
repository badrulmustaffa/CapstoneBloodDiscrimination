# Done by Muhammad Mustaffa and Manuchimso Opara

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextField, SelectField, StringField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class CommentForm(FlaskForm):
    reason = SelectField(choices=['Question', 'Complaint'], validators=[DataRequired()])
    comment = TextField('Comment', widget=TextArea(), validators=[DataRequired()])


class FeedbackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextField('Message', widget=TextArea(), validators=[DataRequired()])


class FeedbackReplyForm(FlaskForm):
    reply = TextField('Reply here')
