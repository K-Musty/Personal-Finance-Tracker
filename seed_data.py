from app import create_app, db
from app.models import User, Transaction, Goal

app = create_app()

with app.app_context():
    # Clear existing data (Optional, be careful)
    db.session.query(Transaction).delete()
    db.session.query(Goal).delete()
    db.session.query(User).delete()

    # Create demo user
    user1 = User(name="John Doe", email="john@example.com", password="1234")
    user2 = User(name="Jane Smith", email="jane@example.com", password="abcd")

    db.session.add_all([user1, user2])
    db.session.commit()

    # Add Transactions for John
    transactions = [
        Transaction(amount=1000, category='income', description='Salary', user_id=user1.id),
        Transaction(amount=-200, category='expense', description='Groceries', user_id=user1.id),
        Transaction(amount=-50, category='expense', description='Transport', user_id=user1.id),
    ]

    # Add Goals for John
    goals = [
        Goal(category='Vacation', amount=5000, user_id=user1.id),
        Goal(category='Emergency Fund', amount=10000, user_id=user1.id)
    ]

    db.session.add_all(transactions + goals)
    db.session.commit()

    print("Demo data seeded successfully!")
