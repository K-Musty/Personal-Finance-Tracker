from flask import Flask
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = "secret-key-secret-key"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/kmusty/Desktop/Projects/Personal-Finance-Tracker/instance/finance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    from app.routes import bp
    app.register_blueprint(bp)

    with app.app_context():
        db.create_all()
    return app