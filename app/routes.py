from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import logout_user, login_user, current_user, confirm_login, login_required
from .extensions import db, login_manager
from .models import User

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('index.html')


@login_required
@bp.route('/dashboard')
def user_dashboard():
    # You need to pass all the variables your template expects
    return render_template('dashboard.html',
        current_balance=1000.00,  # Example - replace with real data
        recent_income=500.00,
        recent_expenses=300.00,
        recent_transactions=[],  # Should be Transaction.query.limit(5).all()
        budgets=[],  # Should be Budget.query.all()
        spending_categories=['Food', 'Transport', 'Entertainment'],
        spending_amounts=[200, 150, 100]
    )
@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form['email']).first()
        login_user(user)  # This is what makes current_user work
        flash("Login Successful !!!")
        return redirect(url_for('main.user_dashboard'))
    return render_template("signup.html")


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        print("YOu don enter o!!!")
        # You need to actually login the user
        user = User.query.filter_by(email=request.form['email']).first()
        if user and (user.password, request.form['password']):
            login_user(user)  # This is what makes current_user work
            flash("Login Successful !!!")
            return redirect(url_for('main.user_dashboard'))
        flash("Invalid credentials")
    return render_template("login.html")

@bp.route("/transactions")
def transactions():
    return "<h1> Hi </h1>"