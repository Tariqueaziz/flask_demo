from flask import jsonify, abort, request
from ..models import User, Role, Post
from . import api
from .. import db

from flask_login import login_required

import logging
from app import create_app
app = create_app('development')

file_handler = logging.FileHandler('api.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)


@api.route('/api/get_users')
def get_users():
  users = User.query.all()
  return jsonify({'users':  [item.serialize() for item in users]})

@api.route('/api/get_roles')
def get_roles():
  roles = Role.query.all()
  return jsonify({'roles':  [item.serialize() for item in roles]})

@api.route('/api/get_posts')
def get_posts():
  posts = Post.query.all()
  return jsonify({'posts':  [item.serialize() for item in posts if item.is_visible == True]})


@api.route('/api/get_post/<int:post_id>', methods = ['GET'])
def get_post(post_id):
  post = Post.query.get(post_id)
  return jsonify({'post': post.serialize()})

@api.route('/api/post', methods=['POST'])
def create_post():
  print(request.json)
  

  post = Post(post=request.json['post'], is_visible = False if ('is_visible' in request.json and request.json['is_visible'] == "False") else True)

  try:
    db.session.add(post)
    db.session.commit()
    return jsonify({'success':True}), 200 
  except:
    return jsonify({'Error': "Couldn't save the post"}), 205

@api.route('/api/post/<int:post_id>', methods = ['PUT'])
def update_post(post_id):
  if (not request.json or not 'post' in request.json):
    abort(400)

  post = Post.query.get(post_id)
  if(post == None):
    return jsonify({'Error': "Post doesn't exist"}), 205
  post.post = request.json['post']
  post.is_visible = False if ('is_visible' in request.json and request.json['is_visible'] == "False") else True

  try:
    db.session.add(post)
    db.session.commit()
    return jsonify({'success':True}), 200 
  except:
    return jsonify({'Error': "Couldn't save the post"}), 205

@api.route('/api/post/<int:post_id>', methods = ['DELETE'])
def delete_post(post_id):
  post = Post.query.get(post_id)
  if (post == None):
    app.logger.error("Post doesn't exist")
    return jsonify({'Error': "Post doesn't exist"}), 205
  try:
    db.session.delete(post)
    db.session.commit()
    app.logger.info("Deleted post: " + post.post)
    return jsonify({'success':True}), 200
  except:
    app.logger.warning("Couldn't delete the post")
    return jsonify({'Error': "Couldn't delete the post"}), 205
