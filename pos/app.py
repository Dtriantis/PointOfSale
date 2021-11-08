from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from api import order
from models import db

def create_app():

    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.register_blueprint(order)

    db.init_app(app)
    with app.app_context():
        db.create_all()

    return app

