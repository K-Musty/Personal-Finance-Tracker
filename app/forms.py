from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, EmailField, FloatField, SelectField
from wtforms.validators import DataRequired, Email

class SignupForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField("Sign Up!!")

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])  # Changed from name+email to just email
    password = PasswordField('Password', validators=[DataRequired()])  # This was missing
    submit = SubmitField('Log In')  # Changed submit text

class TransactionForm(FlaskForm):
    amount = FloatField("Amount", [DataRequired()])
    category = SelectField('Category', choices=[('income','Income'), ('expense','Expense'), ('savings','Savings')])
    description = StringField('Description')
    submit = SubmitField('Add Transaction')

class GoalForm(FlaskForm):
    category = StringField('Goal Category', [DataRequired()])
    amount = FloatField('Target Amount', [DataRequired()])
    submit = SubmitField('Set Goal')
