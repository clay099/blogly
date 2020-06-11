"""Blogly application."""
# run below line when DB have been updated
# db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, request, redirect, render_template
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = 'Secret'
debug = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def home_page():
    return redirect('/users')


@app.route('/users')
def all_users():
    """
    shows all users
    each user has a link to users individual pages
    have a link to create a new user
    """

    users = User.query.all()

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

    return redirect(f'/users/{user.id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """
    deletes the current user
    returns to all user page
    """

    User.query.filter_by(id=user_id).delete()
    # or the following two lines
    # user = User.query.get(user_id)
    # db.session.delete(user)
    db.session.commit()
    return redirect('/users')
