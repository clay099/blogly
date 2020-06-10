from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """test for model for User"""

    def setUp(self):
        """remove any existing users"""
        User.query.delete()

    def tearDown(self):
        """clean up any fouled transactions"""

        db.session.rollback()
