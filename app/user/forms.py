from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
  post = StringField('Post', validators=[DataRequired()])
  submit = SubmitField('Submit')