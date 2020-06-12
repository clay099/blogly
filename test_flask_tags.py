from unittest import TestCase

from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class TagTestCase(TestCase):
    """Tests for users"""

    def setUp(self):
        """add two users"""
        user1 = User(first_name="TestFirstName1", last_name="TestLastName1",
                     image_url="https://ca-times.brightspotcdn.com/dims4/default/1d338c3/2147483647/strip/true/crop/4928x3264+0+0/resize/840x556!/quality/90/?url=https%3A%2F%2Fcalifornia-times-brightspot.s3.amazonaws.com%2F45%2F09%2F7c8d7171490d9c8744534920524a%2Fpet-store-adobestock-285952143.jpeg")

        user2 = User(first_name="TestFirstName2",
                     last_name="TestLastName2", image_url="")

        db.session.add(user1)
        db.session.add(user2)
        db.session.commit()

        self.user1_id = user1.id
        self.user2_id = user2.id

        self.user1 = user1

        post = Post(title="postTitle", content="postContent", user_id=user1.id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

        self.client = app.test_client()

        t1 = Tag(name="Fun")
        t2 = Tag(name="Even More")

        db.session.add_all([t1, t2])
        db.session.commit()

        self.tag_id = t1.id
        self.tag = t1

    def tearDown(self):
        """clean up any transactions"""
        db.session.rollback()
        Post.query.delete()
        Tag.query.delete()

    def test_all_tags_page(self):
        resp = self.client.get('/tags')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Fun', resp.data)

    def test_tag_details_page(self):
        resp = self.client.get(f'/tags/{self.tag_id}')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'No posts have been linked', resp.data)

    def test_tag_new(self):
        resp = self.client.get('/tags/new')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Create a Tag', resp.data)

    def test_tag_new_post(self):
        resp = self.client.post('/tags/new', data={"name": "newTag"})

        self.assertEqual(resp.status_code, 302)

    def test_tag_new_post_follow(self):
        resp = self.client.post(
            '/tags/new', data={"name": "newTag"}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('newTag', html)

    def test_tag_edit(self):
        resp = self.client.get(f'/tags/{self.tag_id}/edit')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Edit a Tag', resp.data)

    def test_tag_edit_post(self):
        resp = self.client.post(
            f'/tags/{self.tag_id}/edit', data={"name": "updated"})

        self.assertEqual(resp.status_code, 302)

    def test_tag_edit_post_follow(self):
        resp = self.client.post(
            f'/tags/{self.tag_id}/edit', data={"name": "updatedTag"}, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'updatedTag', resp.data)

    def test_tag_delet(self):
        tagToDelete = Tag(name="deleteTag")
        db.session.add(tagToDelete)
        db.session.commit()

        resp = self.client.post(
            f'/tags/{tagToDelete.id}/delete', follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(
            b'<p class="alert alert-danger">deleteTag deleted</p>', resp.data)
