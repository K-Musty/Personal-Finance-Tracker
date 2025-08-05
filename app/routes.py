# routes.py
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from .extensions import db
from .models import User, Transaction, Goal
from .forms import TransactionForm, GoalForm, SignupForm, LoginForm
import json
from datetime import datetime

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/dashboard', methods=['GET', 'POST'])
@login_required
def user_dashboard():
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
        return redirect(url_for('main.user_dashboard'))  # PRG pattern

    # Get transactions (newest first)
    transactions = Transaction.query.filter_by(
        user_id=current_user.id
    ).order_by(Transaction.id.desc()).limit(8).all()

    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.category == 'income')
    total_expense = sum(abs(t.amount) for t in transactions if t.category == 'expense')

    # Prepare chart data - group by category
    expenses_by_category = {}
    for t in transactions:
        if t.category == 'expense':
            expenses_by_category[t.category] = expenses_by_category.get(t.category, 0) + abs(t.amount)

    # If no expenses, show empty state
    if not expenses_by_category:
        expenses_by_category = {'No Expenses': 1}

    return render_template('dashboard.html',
        form=form,
        current_balance=total_income - total_expense,
        recent_income=total_income,
        recent_expenses=total_expense,
        recent_transactions=transactions,
        chart_data_json=json.dumps({
            'labels': list(expenses_by_category.keys()),
            'data': list(expenses_by_category.values())
        }))


@bp.route('/get_spending_data')
@login_required
def get_spending_data():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    total_income = sum(t.amount for t in transactions if t.category == 'income')
    total_expense = sum(abs(t.amount) for t in transactions if t.category == 'expense')
    total_savings = sum(abs(t.amount) for t in transactions if t.category == 'savings')

    allocated = total_expense + total_savings
    remaining_balance = total_income - allocated if total_income - allocated > 0 else 0

    chart_data = {
        'labels': ['Expenses', 'Savings', 'Remaining'],
        'data': [total_expense, total_savings, remaining_balance]
    }

    # Fallback if everything is 0
    if sum(chart_data['data']) == 0:
        chart_data = {
            'labels': ['No Data'],
            'data': [1]
        }

    return jsonify(chart_data)

@bp.route("/get_available_months")
@login_required
def get_available_months():
    transactions = Transaction.query.filter_by(user_id=current_user.id).all()

    months = set()
    for t in transactions:
        months.add(t.created_at.strftime('%Y-%m'))

    sorted_months = sorted(list(months), reverse=True)

    return jsonify(sorted_months)


@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user:
            flash("Email already exists. Please log in.", 'error')
            return redirect(url_for('main.login'))

        new_user = User(
            name=form.name.data,
            email=form.email.data
        )
        new_user.set_password(form.password.data)  # Hashes the password
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created successfully!", 'success')
        return redirect(url_for('main.user_dashboard'))

    return render_template("signup.html", form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):  # Secure check
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('main.user_dashboard'))
        flash('Invalid email or password', 'error')
    return render_template('login.html', form=form)

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect(url_for('main.index'))

@bp.route('/add_transaction', methods=['GET', 'POST'])
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
        print("Transaction works")
    return redirect(url_for('main.user_dashboard', form=form))

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
    return redirect(url_for('main.user_dashboard', form=form))

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
