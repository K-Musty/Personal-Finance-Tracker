from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField("Name", [DataRequired()])
    email = EmailField('Email', [DataRequired()])
    password = PasswordField('Password', [DataRequired()])
    submit = SubmitField("Sign Up!!")

class LoginForm(FlaskForm):
    name = StringField("Name ", validators=[DataRequired()])
    email = EmailField("Email ", validators=[DataRequired()])
    submit = SubmitField("Let me in !!")

class TransactionForm(FlaskForm):
    amount = FloatField("Amount", [DataRequired()])
    category = SelectField('Category', choices=[('income','Income'), ('expense','Expense'), ('savings','Savings')])
    description = StringField('Description')
    submit = SubmitField('Add Transaction')

class GoalForm(FlaskForm):
    category = StringField('Goal Category', [DataRequired()])
    amount = FloatField('Target Amount', [DataRequired()])
    submit = SubmitField('Set Goal')
