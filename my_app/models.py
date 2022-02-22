# Done by Muhammad Mustaffa
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from my_app import db
from datetime import datetime


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    email = db.Column(db.Text, unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        return f"{self.id} {self.username} {self.email} {self.password}"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Profile(db.Model):
    __tablename__ = "profile"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True, nullable=False)
    bio = db.Column(db.Text)
    photo = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class History(db.Model):
    __tablename__ = "history"
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column('created_on', db.DateTime, default=datetime.utcnow())
    mean = db.Column(db.Text)
    start = db.Column(db.Text)
    end = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Blogpost(db.Model):
    __tablename__ = "blogpost"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Forum(db.Model):
    __tablename__ = "forum"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.Text)
    reason = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)


class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text)
    subject = db.Column(db.Text)
    message = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)


class FeedbackReply(db.Model):
    __tablename__ = "feedbackreply"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False)
    reply = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)
    feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Trial(db.Model):
    __tablename__ = "trial"
    id = db.Column(db.Integer, primary_key=True)
    registration_number = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)

class Tester(db.Model):
    __tablename__ = "tester"
    id = db.Column(db.Integer, primary_key=True)
    kit_id = db.Column(db.Integer)
    blood_image = db.Column(db.Text)
    result = db.Column(db.Text)
    # date_posted = db.Column(db.DateTime)


class ShoppingCart(db.Model):
    __tablename__ = 'shopping cart'
    id = db.Column(db.Integer)
    username = db.Column(db.Text, nullable=False, primary_key=True)
    QuantityA = db.Column(db.Integer)
    QuantityB = db.Column(db.Integer)

