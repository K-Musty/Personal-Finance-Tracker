from flask import Blueprint, render_template, redirect, url_for, flash, request
# from forms import LoginForm, SignupForm, TransactionForm
# from models import User
from flask_login import logout_user, login_user, current_user, confirm_login, login_required

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@login_required
@bp.route('/dashboard')
def user_dashboard():
    return render_template('dashboard.html')

@bp.route('/signup')
def signup():
    return render_template("signup.html")

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        flash("Login Successful !!!")
        return redirect(url_for('main.user_dashboard'))
    return render_template("login.html")