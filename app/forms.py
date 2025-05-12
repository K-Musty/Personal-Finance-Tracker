from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, PasswordField, FloatField, SelectField
from wtforms.validators import DataRequired

class SignupForm(FlaskForm):
    name = StringField("name", [DataRequired()])
    email = EmailField('email', [DataRequired()])
    password = PasswordField('password', [DataRequired()])
    submit = SubmitField()

class TransactionForm(FlaskForm):
    amount = FloatField("Amount", [DataRequired()])
    category = SelectField('Category', choices=[('income','Income'), ('expense','Expense'), ('savings','Savings')])
    description = StringField('Description')
    submit = SubmitField('Add Transaction')