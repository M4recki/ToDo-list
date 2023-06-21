from flask import Flask, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from forms import CreateToDo, RegisterForm, LoginForm, ContactForm
from os import environ


app = Flask(__name__)

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY_TODO')

Bootstrap(app)

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///ToDo.db"
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
@login_required
def create():
    form = CreateToDo()
    if form.validate_on_submit():
        priority = form.priority.data
        title = form.title.data
        content = form.content.data
        user_id = current_user.id
        
        new_todo = ToDo(priority=priority, title=title, content=content, user_id=user_id)
        
        if ToDo.query.filter_by(title=title).first():
            flash('Title already exists. Please type a different title.')
            return redirect(url_for('create'))
        
        db.session.add(new_todo)
        db.session.commit()
        
        return redirect(url_for('home_page'))
    
    return render_template('create_todo_page.html', form=form)

@app.route('/all_todos')
@login_required
def all_todos():
    # todos = ToDo.query.all()
    return render_template('all_todos_page.html')

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
            return redirect(url_for('home_page', name=User.first_name))

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

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home_page'))

# Load user
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


if __name__ == '__main__':
    app.run(debug=True)