import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# define sqlite database file path 
db_dir = os.path.abspath('data.sqlite')

# app settings 
app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config["DEBUG"] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)