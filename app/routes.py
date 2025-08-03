# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from .extensions import db
from .models import User, Transaction, Goal
from .forms import TransactionForm, GoalForm

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/get_spending_data')
@login_required
def get_spending_data():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    category_spending = {}
    for t in transactions:
        if t.category != 'income':
            category_spending[t.description] = category_spending.get(t.description, 0) + abs(t.amount)

    # Ensure there's always data to show
    if not category_spending:
        category_spending = {'No Data': 1}

    return jsonify({
        'labels': list(category_spending.keys()),
        'data': list(category_spending.values())
    })

@bp.route('/dashboard')
@login_required
def user_dashboard():
    transaction_form = TransactionForm()

    transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.id.desc()).limit(5).all()

    total_income = sum(t.amount for t in transactions if t.category == 'income')
    total_expense = sum(t.amount for t in transactions if t.category == 'expense')

    # Spending grouped by description for chart
    category_spending = {}
    for t in transactions:
        if t.category != 'income':
            category_spending[t.description] = category_spending.get(t.description, 0) + abs(t.amount)

    if not category_spending:
        category_spending = {'No Data': 1}

    return render_template('dashboard.html',
                           form=transaction_form,
                           current_balance=total_income - total_expense,
                           recent_income=total_income,
                           recent_expenses=total_expense,
                           recent_transactions=transactions,
                           spending_categories=list(category_spending.keys()),
                           spending_amounts=list(category_spending.values()))


@bp.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == "POST":
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Email already exists. Please log in.")
            return redirect(url_for('main.login'))

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Signup Successful! You are now logged in.")
        return redirect(url_for('main.user_dashboard'))

    return render_template("signup.html")


@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(email=request.form['email']).first()
        if user and (user.password == request.form['password']):
            login_user(user)
            flash("Login Successful !!!")
            return redirect(url_for('main.user_dashboard'))
        flash("Invalid credentials")
    return render_template("login.html")

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))

@bp.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    form = TransactionForm()
    if form.validate_on_submit():
        transaction = Transaction(
            amount=form.amount.data,
            category=form.category.data,
            description=form.description.data,
            user_id=current_user.id
        )
        db.session.add(transaction)
        db.session.commit()
        flash("Transaction added!")
    return redirect(url_for('main.user_dashboard'))

@bp.route('/add_goal', methods=['POST'])
@login_required
def add_goal():
    form = GoalForm()
    if form.validate_on_submit():
        goal = Goal(
            category=form.category.data,
            amount=form.amount.data,
            user_id=current_user.id
        )
        db.session.add(goal)
        db.session.commit()
        flash("Goal added successfully!")
    return redirect(url_for('main.user_dashboard'))

@bp.route('/budgets')
@login_required
def budgets():
    return "<h1>Budgets Page Placeholder</h1>"

@bp.route('/reports')
@login_required
def reports():
    return "<h1>Reports Page (Coming Soon)</h1>"

@bp.route('/goals')
@login_required
def goals():
    return "<h1>Goals Page (Coming Soon)</h1>"

@bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
