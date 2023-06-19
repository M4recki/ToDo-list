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
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User, backref='todos')

    

# Home page
@app.route('/')
def home_page():
    return render_template('home_page.html')

# Create ToDo
@app.route('/create', methods=['GET', 'POST'])
def create():
    form = CreateToDo()
    if form.validate_on_submit():
        return redirect(url_for('home_page'))
    
    return render_template('create_todo_page.html', form=form)

# Sign up
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=9)
        
        new_user = User(first_name=first_name, last_name=last_name, email=email, password=hashed_password)
        
        if User.query.filter_by(email=email).first():
            flash('Email already exists. Please login or use a different email.')
            return redirect(url_for('signup'))
        
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)
        
        return redirect(url_for('home_page'))
    
    return render_template('sign_up_page.html', form=form)


# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        
        user = User.query.filter_by(email=email).first()
        if not user:
            flash('Email does not exist. Please register.')
            return redirect(url_for('login'))
        elif not check_password_hash(user.password, password):
            flash('Incorrect password. Please try again.')
            return redirect(url_for('login'))
        else:
            login_user(user)
            return redirect(url_for('home_page', name='placeholder'))

    return render_template('login_page.html', form=form)

# Contact
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        message = form.message.data
        
        return redirect(url_for('home_page'))

    return render_template('contact_page.html', form=form)

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)