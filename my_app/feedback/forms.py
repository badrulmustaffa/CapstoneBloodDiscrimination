# Done by Muhammad Mustaffa and Manuchimso Opara

from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, SelectField, StringField, EmailField
# from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired
from wtforms.widgets import TextArea


class CommentForm(FlaskForm):
    reason = SelectField(choices=['Question', 'Complaint'], validators=[DataRequired()])
    comment = TextAreaField('Comment', widget=TextArea(), validators=[DataRequired()])


class FeedbackForm(FlaskForm):
    subject = StringField('Subject', validators=[DataRequired()])
    message = TextAreaField('Message', widget=TextArea(), validators=[DataRequired()])


class FeedbackReplyForm(FlaskForm):
    reply = TextAreaField('Reply here')
