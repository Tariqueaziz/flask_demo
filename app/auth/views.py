from flask import flash, redirect, render_template, url_for
from flask_login import login_required, login_user, logout_user

from . import auth
from forms import LoginForm, RegistrationForm
from .. import db
from ..models import User



@auth.route('/register', methods=['GET', 'POST'])
def register():
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(email=form.email.data,
                        username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        password=form.password.data)

    # add user to the database
    db.session.add(user)
    db.session.commit()
    flash('User registered.')

    # redirect to the login page
    return redirect(url_for('auth.login'))

  # load registration template
  return render_template('auth/register.html', form=form, title='Register')

@auth.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():

    user = User.query.filter_by(email=form.email.data).first()
    if user is None:
      flash('Invalid email')
    elif user is not None and user.verify_password(form.password.data):
      login_user(user)
      if user.is_admin:
        return redirect(url_for('home.admin_dashboard'))
      else:
        return redirect(url_for('home.dashboard'))
    else:
      flash('Invalid password.')

  return render_template('auth/login.html', form=form, title='Login')

@auth.route('/logout')
@login_required
def logout():

  logout_user()
  flash('Logged out.')

  # redirect to the login page
  return redirect(url_for('auth.login'))