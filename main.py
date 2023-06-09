from flask import Flask, render_template, request, redirect, url_for, flash, abort, session, request
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from flask_gravatar import Gravatar
from functools import wraps
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import psycopg2

app = Flask(__name__)

Bootstrap(app)


@app.route('/')
def home_page():
    return render_template('start_page.html')

@app.route('/signup')
def signup():
    return render_template('sign_up_page.html')


if __name__ == '__main__':
    app.run(debug=True)
