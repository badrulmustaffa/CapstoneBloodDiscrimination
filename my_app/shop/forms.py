
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired, EqualTo, ValidationError

from my_app.models import User


class ShoppingCartForm(FlaskForm):
    username = StringField('Name')
    QuantityA = IntegerField('Product A amount')
    QuantityB = IntegerField('Product B amount')
