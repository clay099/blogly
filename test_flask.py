from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserTestCase(TestCase):
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

    def tearDown(self):
        """clean up any transactions"""
        db.session.rollback()

    def test_users_page(self):
        """test users page"""

        resp = self.client.get('/users')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('TestFirstName1', html)

    def test_new_user(self):
        """test user edit page"""

        resp = self.client.get('/users/new')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Enter a first name', html)

    def test_new_user_post(self):
        """test user edit page"""

        resp = self.client.post(
            '/users/new', data={"firstName": "testFirstName", "lastName": "testLastName", "url": ""})
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 302)

    def test_single_user_page(self):
        """test user page"""

        resp = self.client.get(f'/users/{self.user1_id}')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('TestFirstName1', html)

    def test_user_no_URL(self):
        """test user page with no url"""

        resp = self.client.get(f'/users/{self.user2_id}')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('picture unavalaible', html)

    def test_user_edit(self):
        """test user edit page"""

        resp = self.client.get(f'/users/{self.user1_id}/edit')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn('Edit a User', html)
        self.assertIn(self.user1.first_name, html)

    def test_user_edit_no_user(self):
        """test user edit page where user does not exist"""
        resp = self.client.get('users/10000000/edit')

        self.assertEqual(resp.status_code, 404)

    def test_user_edit_post(self):
        """test user edit post request"""
        resp = self.client.post(f'users/{self.user1_id}/edit', data={
            "firstName": "TestFirstName1", "lastName": "TestFirstName2", "url": ""})

        self.assertEqual(resp.status_code, 302)

    def test_user_edit_post_follow(self):
        """test user edit post request"""
        resp = self.client.post(f'users/{self.user1_id}/edit', data={
            "firstName": "TestFirstName2Update", "lastName": "TestFirstName2Update", "url": ""}, follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn("TestFirstName2Update", html)

    def test_user_delete(self):
        """test delete function"""
        userToDelete = User(first_name="firstDeleteMe",
                            last_name="lastDeleteMe", image_url="")

        db.session.add(userToDelete)
        db.session.commit()

        resp = self.client.post(
            f'/users/{userToDelete.id}/delete', follow_redirects=True)
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('firstDeleteMe', html)

    def test_new_post(self):
        resp = self.client.get(f'/users/{self.user1_id}/posts/new')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Add Post for', resp.data)

    def test_new_post_db(self):
        resp = self.client.post(
            f'/users/{self.user1_id}/posts/new', data={"title": "title", "content": "content"})

        self.assertEqual(resp.status_code, 302)

    def test_new_post_db_follow(self):
        resp = self.client.post(
            f'/users/{self.user1_id}/posts/new', data={"title": "postTitle", "content": "postContent"}, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b"postTitle", resp.data)

    def test_post_details(self):
        resp = self.client.get(f'/posts/{self.post_id}')

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Date Created', resp.data)

    def test_no_post_id_details(self):
        resp = self.client.get(f'/posts/10000000000000')

        self.assertEqual(resp.status_code, 404)

    def test_edit_post(self):
        resp = self.client.get(f'/posts/{self.post_id}/edit')
        html = resp.get_data(as_text=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(self.post.title, html)

    def test_edit_post_db(self):
        resp = self.client.post(f'/posts/{self.post_id}/edit',  data={
                                "title": "postTitleUpdated", "content": "postContentUpdated"})

        self.assertEqual(resp.status_code, 302)

    def test_edit_post_db(self):
        resp = self.client.post(f'/posts/{self.post_id}/edit', data={
                                "title": "postTitleUpdated", "content": "postContentUpdated"}, follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'postTitleUpdated', resp.data)

    def test_delete_posts(self):
        postToDelete = Post(title="postTitleToDelete",
                            content="postContentToDelete", user_id=self.user1.id)

        db.session.add(postToDelete)
        db.session.commit()

        resp = self.client.post(
            f'/posts/{postToDelete.id}/delete', follow_redirects=True)

        self.assertEqual(resp.status_code, 200)
        self.assertNotIn(b'postTitleToDelete', resp.data)
