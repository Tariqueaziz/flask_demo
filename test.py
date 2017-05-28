import unittest
import os

from flask import abort, url_for
from flask_testing import TestCase

from app import create_app, db
from app.models import User, Post, Role

class TestBase(TestCase):

  def create_app(self):
    config_name = 'testing'
    app = create_app(config_name)
    app.config.update(
      SQLALCHEMY_DATABASE_URI='mysql://flask:flask@127.0.0.1:3306/flaskdb_test'
    )
    return app

  def setUp(self):
    db.create_all()
    admin = User(username="admin", password="admin", is_admin=True)

    user = User(username="user", password="user")
    user2 = User(username="user2", password="user2")

    db.session.add(admin)
    db.session.add(user)
    db.session.add(user2)
    db.session.commit()

  def tearDown(self):
    db.session.remove()
    db.drop_all()

class TestModels(TestBase):

  def test_user_model(self):
    self.assertEqual(User.query.count(), 3)

  def test_post_model(self):
    post = Post(post="tweet")

    db.session.add(post)
    db.session.commit()

    self.assertEqual(Post.query.count(), 1)

  def test_role_model(self):
    role = Role(name="BI", description="Business Intelligence")
    db.session.add(role)
    db.session.commit()

    self.assertEqual(Role.query.count(), 1)

class TestViews(TestBase):

  def test_homepage_view(self):
    response = self.client.get(url_for('home.homepage'))
    self.assertEqual(response.status_code, 200)

  def test_login_view(self):
    response = self.client.get(url_for('auth.login'))
    self.assertEqual(response.status_code, 200)

class TestApi(TestBase):
  def test_get_post(self):
    rs = self.app.test_client.get('/api/get_posts')
    self.assertEqual(res.status_code, 200)

if __name__ == '__main__':
  unittest.main()