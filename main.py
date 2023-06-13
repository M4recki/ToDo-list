from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint, create_engine, ForeignKey, Column, String, Integer, CHAR
from sqlalchemy.ext.declarative import declarative_base
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreateToDo, RegisterForm, LoginForm, ContactForm
from flask_gravatar import Gravatar
from functools import wraps
from flask import session
from flask import request
from os import environ


app = Flask(__name__)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY_TODO')

Bootstrap(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# User table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    
# ToDos table
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    priority = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(250), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    

# Home page
@app.route('/')
def home_page():
    return render_template('home_page.html')

# Create ToDo
@app.route('/create')
def create():
    return render_template('create_todo_page.html')

# Sign up
@app.route('/signup')
def signup():
    return render_template('sign_up_page.html')

# Login
@app.route('/login')
def login():
    return render_template('login_page.html')

# Contact
@app.route('/contact')
def contact():
    return render_template('contact_page.html')

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)