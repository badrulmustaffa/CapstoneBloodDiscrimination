# Done by Muhammad Mustaffa

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField, EmailField
# from wtforms.fields.html5 import Emailfield
from wtforms.validators import DataRequired, EqualTo, ValidationError

from my_app.models import User


class SignupForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    email = EmailField(label='Email address', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    password_repeat = PasswordField(label='Repeat Password',
                                    validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    type = SelectField(label='Account type', choices=['User', 'Admin', 'LabTech'])

    def validate_email(self, email):
        users = User.query.filter_by(email=email.data).first()
        if users is not None:
            raise ValidationError("An account is already registered for that email")

    def validate_username(self, username):
        users = User.query.filter_by(username=username.data).first()
        if users is not None:
            raise ValidationError("An account is already registered for that username")


class LoginForm(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    remember = BooleanField(label='Remember me')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("No account found")

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            raise ValidationError("No account found.")
        if not user.check_password(password.data):
            raise ValidationError("Wrong password.")
