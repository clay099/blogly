"""Blogly application."""


from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template, flash
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'Secret'
debug = DebugToolbarExtension(app)

connect_db(app)

# run below line when DB have been updated
# db.create_all()
# see updated seeds.py file when you want to update


@app.errorhandler(404)
def page_not_found(e):
    """
    custom 404 error page
    """

    return render_template('404.html'), 404


@app.route('/')
def home_page():
    """
    renders last 5 posts
    """

    posts = Post.query.order_by(Post.id.desc()).limit(5).all()
    return render_template('home.html', posts=posts)


@app.route('/users')
def all_users():
    """
    shows all users
    each user has a link to users individual pages
    have a link to create a new user
    """

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template('all_users.html', users=users)


@app.route('/users/new')
def new_user_form():
    """add form for a new user"""

    return render_template('create_user.html')


@app.route('/users/new', methods=['POST'])
def add_new_user():
    """
    process the form and adds a new user to db
    returns to users page
    """

    first_name = request.form['firstName']
    last_name = request.form.get('lastName')
    image_url = request.form.get('url', None)

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)
    db.session.add(user)
    db.session.commit()

    flash(f'{user.full_name} created', 'alert alert-success')

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>')
def user_details(user_id):
    """
    shows information about current user
    have buttons to edit or delete the user
    """

    user = User.query.get_or_404(user_id)

    return render_template('user_details.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_user_form(user_id):
    """
    edit form for current user
    cancel to return to user details
    save updated details in form
    """

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def submit_edited_user(user_id):
    """
    process the saved edit user form
    returns to user page
    """
    user = User.query.get(user_id)

    user.first_name = request.form['firstName']
    user.last_name = request.form.get('lastName')
    user.image_url = request.form.get('url', None)

    db.session.add(user)
    db.session.commit()

    flash(f'{user.full_name} edited', 'alert alert-success')

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    deletes the current user
    returns to all user page
    """
    user = User.query.get(user_id)

    db.session.delete(user)
    db.session.commit()

    flash(f'User: {user.full_name} deleted', 'alert alert-danger')

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def new_post_form(user_id):
    """
    form to allow for a new post to be added
    """

    user = User.query.get(user_id)

    return render_template('post_form.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def add_post(user_id):
    """
    adds users post to db
    redirects to user detail page
    """

    title = request.form.get('title')
    content = request.form.get('content')
    # date = datetime.now()

    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

    flash(f'{post.title} created', 'alert alert-success')

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def post_details(post_id):
    """
    shows a post 
    buttons to allows for user to edit and delete the post
    """

    post = Post.query.get_or_404(post_id)

    return render_template('post_details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
    """
    shows form to edit a post
    """

    post = Post.query.get_or_404(post_id)

    return render_template('edit_post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def submit_edited_post(post_id):
    """
    submits edited post to db
    redirects back to user view
    """
    post = Post.query.get_or_404(post_id)

    post.title = request.form.get('title')
    post.content = request.form.get('content')

    db.session.add(post)
    db.session.commit()

    flash(f'{post.title} edited', 'alert alert-success')

    return redirect(f'/users/{post.users.id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """
    deletes the post
    redirects back to all users
    """
    post = Post.query.filter(Post.id == post_id).first()
    user_id = post.user_id

    db.session.delete(post)
    db.session.commit()

    flash(f'Post: {post.title} deleted', 'alert alert-danger')
    return redirect(f'/users/{user_id}')
