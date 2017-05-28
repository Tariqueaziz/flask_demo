from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from forms import RoleForm, UserAssignForm
from .. import db
from ..models import Role, User

from . import admin




def check_admin():
  if not current_user.is_admin:
    flash("User not admin")

@admin.route('/roles')
@login_required
def list_roles():
  check_admin()
  roles = Role.query.all()
  return render_template('admin/roles/roles.html', roles=roles, title='Roles')

@admin.route('/roles/add', methods=['GET', 'POST'])
@login_required
def add_role():
  check_admin()

  add_role = True

  form = RoleForm()
  if form.validate_on_submit():
    role = Role(name=form.name.data, description=form.description.data)

    try:
      db.session.add(role)
      db.session.commit()
      flash('Role Added.')
    except:
      flash('Error: role name already exists.')

    return redirect(url_for('admin.list_roles'))

  return render_template('admin/roles/role.html', add_role=add_role, form=form, title='Add Role')

@admin.route('/roles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
  check_admin()

  add_role = False

  role = Role.query.get_or_404(id)
  form = RoleForm(obj=role)
  if form.validate_on_submit():
    role.name = form.name.data
    role.description = form.description.data
    db.session.add(role)
    db.session.commit()
    flash('Role Edited.')
    return redirect(url_for('admin.list_roles'))

  form.description.data = role.description
  form.name.data = role.name
  return render_template('admin/roles/role.html', add_role=add_role, form=form, title="Edit Role")

@admin.route('/roles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_role(id):
  check_admin()

  role = Role.query.get_or_404(id)
  db.session.delete(role)
  db.session.commit()
  flash('Role Deleted.')

  return redirect(url_for('admin.list_roles'))

  # return render_template(title="Delete Role")



@admin.route('/users')
@login_required
def list_users():
  check_admin()
  users = User.query.all()
  return render_template('admin/users/users.html', users=users, title='Users')

@admin.route('/users/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_user(id):
  check_admin()

  user = User.query.get_or_404(id)

  if user.is_admin:
    flash("User is Admin.")

  form = UserAssignForm(obj=user)
  if form.validate_on_submit():
    user.role = form.role.data
    db.session.add(user)
    db.session.commit()
    flash('Role Assigned for user')

    return redirect(url_for('admin.list_users'))

  return render_template('admin/users/user.html', user=user, form=form, title='Assign User')