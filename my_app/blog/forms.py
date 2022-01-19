# Done by Muhammad Mustaffa and Farhan Basir Ul' Elmi

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField

class BlogForm(FlaskForm):
    """ Class for the blog form """
    title = StringField(label='Title', description='Write something about yourself')
    subtitle = StringField(label='Subtitle', description='Write something about yourself')
    author = StringField(label='Author', description='Write something about yourself')
    content = TextAreaField(label='Blog content', description='Write something about yourself')
