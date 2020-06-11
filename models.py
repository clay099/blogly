"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """connect to database"""

    db.app = app
    db.init_app(app)


class User(db.Model):
    """Users Class"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True)
    first_name = db.Column(db.String,
                           nullable=False)
    last_name = db.Column(db.String,
                          nullable=False)
    image_url = db.Column(db.String)

    @ property
    def full_name(self):
        """returns fullname of user"""
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        """show information about users"""

        u = self
        return f"< User {u.first_name} {u.last_name} {u.image_url}>"


class Post(db.Model):
    """Post Class"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey(users.id))

    users = db.relationship('User', backref='posts')
