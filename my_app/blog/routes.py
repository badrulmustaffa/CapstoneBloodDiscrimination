# Done by Muhammad Mustaffa and Farhan Basir Ul' Elmi

from flask import render_template, request, redirect, url_for, Blueprint
from datetime import datetime
from flask_login import login_required, current_user

from my_app import db
from my_app.blog.forms import BlogForm
from my_app.models import Blogpost

blog_bp = Blueprint('blog_bp', __name__, url_prefix='/blog')


@blog_bp.route('/')
@login_required
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()

    return render_template('blog_index.html', posts=posts)


@blog_bp.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()

    return render_template('blog_post.html', post=post)


@blog_bp.route('/about')
def about():
    return render_template('blog_about.html')


@blog_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = BlogForm()
    if request.method == 'POST':
        post = Blogpost(title=form.title.data, subtitle=form.subtitle.data,
                        author=current_user.username, user_id=current_user.id,
                        content=form.content.data, date_posted=datetime.now())
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('blog_bp.index'))
    return render_template('blog_add.html', form=form, author=current_user.username)


