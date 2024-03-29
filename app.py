"""Blogly application."""

from flask import Flask, request, redirect, render_template, flash, session
from models import db, connect_db, User,Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///Users2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "Godalone1."
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.drop_all()
db.create_all()

@app.route('/')
def welcome():
    return redirect('/users')

@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('home.html', users=users)

@app.route('/users/new')
def user_form():
    return render_template('create-user-form.html')

@app.route('/users/new',methods = ['POST'])
def creating_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    new_user = User(first_name = first_name, last_name = last_name, image_url = image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>')
def details(user_id):
    user = User.query.get(user_id)
    return render_template('detail.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    user = User.query.get(user_id)
    return render_template('edit-user-form.html', user=user)

@app.route('/users/<int:user_id>/edit', methods = ['POST'])
def edit_user(user_id):
    new_first_name = request.form['first_name']
    new_last_name = request.form['last_name']
    new_image_url = request.form['image_url']
    user = User.query.get(user_id)
    if new_first_name:
        user.first_name = new_first_name 
    if new_last_name:
        user.last_name = new_last_name 
    if new_image_url:
        user.image_url = new_image_url
    db.session.add(user)
    db.session.commit()
    return redirect(f"/users/{user_id}")

@app.route('/users/<int:user_id>/delete')
def delete(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    user = User.query.get(user_id)
    return render_template('post_form.html',user=user)

@app.route('/users/<int:user_id>/posts/new', methods = ['POST'])
def make_form(user_id):
    title = request.form['title']
    content = request.form['content']
    new_post = Post(title = title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    post = Post.query.get(post_id)
    return render_template('post.html',post=post)

@app.route('/posts/<int:post_id>/edit')
def show_edit_form(post_id):
    post = Post.query.get(post_id)
    return render_template('edit_post_form.html',post=post)

@app.route('/posts/<int:post_id>/edit', methods =['POST'])
def edit_post(post_id):
    post = Post.query.get(post_id)
    if request.form['title']:
        new_title = request.form['title']
        post.title = new_title
    if request.form['content']:
        new_content = request.form['content']
        post.content = new_content
    db.session.add(post)
    db.session.commit()
    return redirect(f'/posts/{post_id}')

@app.route('/posts/<int:post_id>/delete', methods = ['POST'])
def delete_post(post_id):
    post = Post.query.filter_by(id=post_id).first()
    post_id = post.user.id
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()
    return redirect(f'/users/{post_id}')