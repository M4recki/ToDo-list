from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm,  RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from flask import session
from flask import request
from os import environ
import psycopg2


app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY_TODO')

Bootstrap(app)


@app.route('/')
def home_page():
    return render_template('home_page.html')

@app.route('/create')
def create():
    return render_template('create_todo_page.html')

@app.route('/signup')
def signup():
    return render_template('sign_up_page.html')

@app.route('/login')
def login():
    return render_template('login_page.html')

@app.route('/contact')
def contact():
    return render_template('contact_page.html')


if __name__ == '__main__':
    app.run(debug=True)
