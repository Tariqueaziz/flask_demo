from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager




class User(UserMixin, db.Model):

  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String(60), index=True, unique=True)
  username = db.Column(db.String(60), index=True, unique=True)
  first_name = db.Column(db.String(60), index=True)
  last_name = db.Column(db.String(60), index=True)
  password_hash = db.Column(db.String(128))
  role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
  is_admin = db.Column(db.Boolean, default=False)
  posts = db.relationship('Post', backref='user', lazy='dynamic')


  def serialize(self):
    return {
      'email' : self.email,
      'username' : self.username,
      'first_name' : self.first_name,
      'last_name' : self.last_name
    }
    

  @property
  def password(self):
    raise AttributeError('password is not a readable attribute.')

  @password.setter
  def password(self, password):
    self.password_hash = generate_password_hash(password)

  def verify_password(self, password):
    return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))



class Role(db.Model):
  __tablename__ = 'roles'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(60), unique=True)
  description = db.Column(db.String(200))
  users = db.relationship('User', backref='role', lazy='dynamic')

  def serialize(self):
    return {
      'name' : self.name,
      'description' : self.description
    }


class Post(db.Model):
  __tablename__ = 'posts'

  id = db.Column(db.Integer, primary_key=True)
  post = db.Column(db.String(60))
  is_visible = db.Column(db.Boolean, default=True)
  user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

  def serialize(self):
    return {
      'post' : self.post,
      'is_visible' : self.is_visible
    }
