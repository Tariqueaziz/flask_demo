from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from forms import PostForm
from .. import db
from ..models import Post

from . import user


@user.route('/posts', methods=['GET', 'POST'])
@login_required
def list_posts():

  posts = Post.query.all()

  return render_template('posts/posts.html', posts=posts, title="Posts")

@user.route('/posts/add', methods=['GET', 'POST'])
@login_required
def add_post():

  add_post = True

  form = PostForm()
  if form.validate_on_submit():
    post = Post(post=form.post.data)
    try:
      # add post to the database
      db.session.add(post)
      db.session.commit()
      flash('You have successfully added a new post.')
    except:
      # in case post name already exists
      flash('Error:')

    # redirect to posts page
    return redirect(url_for('user.list_posts'))

  # load post template
  return render_template('posts/post.html', action="Add", add_post=add_post, form=form, title="Add Post")

@user.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_post(id):

  add_post = False

  post = Post.query.get_or_404(id)
  form = PostForm(obj=post)
  if form.validate_on_submit():
    post.post = form.post.data
    db.session.commit()
    flash('You have successfully edited the post.')

    # redirect to the users page
    return redirect(url_for('user.list_posts'))

  form.post.data = post.post
  return render_template('posts/post.html', action="Edit", add_post=add_post, form=form, post=post, title="Edit Post")

@user.route('/posts/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_post(id):
  post = Post.query.get_or_404(id)
  db.session.delete(post)
  db.session.commit()
  flash('You have successfully deleted the post.')
  return redirect(url_for('user.list_posts'))

  # return render_template(title="Delete Post")