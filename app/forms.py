from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField("name", [DataRequired()])
    email = EmailField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    submit = SubmitField()