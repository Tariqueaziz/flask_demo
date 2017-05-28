from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired

from ..models import Role


class RoleForm(FlaskForm):
  name = StringField('Name', validators=[DataRequired()])
  description = StringField('Description', validators=[DataRequired()])
  submit = SubmitField('Submit')


class UserAssignForm(FlaskForm):
  role = QuerySelectField(query_factory=lambda: Role.query.all(), get_label="name")
  submit = SubmitField('Submit')