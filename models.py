"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """connect to database"""

    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"


class User(db.Model):
    """Users Class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String,
                           nullable=False)
    last_name = db.Column(db.String,
                          nullable=False, default=DEFAULT_IMAGE_URL)
    image_url = db.Column(db.String)

    @ property
    def full_name(self):
        """returns fullname of user"""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        """show information about users"""

        u = self
        return f"< User ID={u.id} First_name={u.first_name} Last_name={u.last_name} Image_url={u.image_url} >"


class Post(db.Model):
    """Post Class"""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)

    date = datetime.now()
    format_date = date.strftime("%B %d %Y")
    created_at = db.Column(db.DateTime, nullable=False, default=format_date)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    users = db.relationship("User", backref=db.backref(
        "posts", cascade="all, delete-orphan"))

    def __repr__(self):
        """show information about users"""

        p = self
        return f"< Post ID={p.id} Title={p.title} Content={p.content} Created_at={p.created_at} User_id={p.user_id} >"


class Tag(db.Model):
    """Tag Class"""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship('Post', secondary='post_tag', backref='tags')

    def __repr__(self):
        t = self
        return f'< Tag ID={t.id} Name={t.name} >'


class PostTag(db.Model):
    """PostTag Class"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

    def __repr__(self):
        t = self
        return f'< PostTag Post_id={t.post_id} Tag_id={t.tag_id} >'
