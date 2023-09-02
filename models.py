from extensions import app, db
from os import environ
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin
from flask import flash

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
    title = db.Column(db.String(25), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = relationship(User, backref='todos')

    def is_title_valid(self):
        max_title_length = 25

        if len(self.title) > max_title_length:
            flash('Title is too long. Please type a shorter title.')
            return False