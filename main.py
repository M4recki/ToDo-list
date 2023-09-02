from extensions import app, db
from forms import CreateToDo, RegisterForm, LoginForm, ContactForm
from models import ToDo, User
from flask import Flask, render_template, redirect, url_for, flash, get_flashed_messages
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from os import environ
from datetime import datetime
import smtplib
from email.message import EmailMessage
import ssl


# Login manager


login_manager = LoginManager()
login_manager.init_app(app)

app.config['SECRET_KEY'] = environ.get('SECRET_KEY_TODO')

Bootstrap(app)

# Current year in footer


@app.context_processor
def current_year():
    current_year = datetime.now().year
    return {'current_year': current_year}

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

        new_todo = ToDo(priority=priority, title=title,
                        content=content, user_id=user_id)

        if ToDo.query.filter_by(title=title).first():
            flash('Title already exists. Please type a different title.')
            return redirect(url_for('create'))

        db.session.add(new_todo)
        db.session.commit()

        return redirect(url_for('all_todos'))

    return render_template('create_todo_page.html', form=form)

# Edit ToDo


@app.route('/edit/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def edit(todo_id):
    todo = ToDo.query.get(todo_id)
    form = CreateToDo(priority=todo.priority,
                      title=todo.title, content=todo.content)

    if form.validate_on_submit():
        priority = form.priority.data
        title = form.title.data
        content = form.content.data

        todo.priority = priority
        todo.title = title
        todo.content = content

        db.session.commit()

        return redirect(url_for('home_page'))

    return render_template('edit_todo_page.html', form=form, todo_id=todo_id)

# Delete ToDo


@app.route('/delete/<int:todo_id>', methods=['GET', 'POST'])
@login_required
def delete(todo_id):
    todo_to_delete = ToDo.query.get(todo_id)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect(url_for('all_todos'))


@app.route('/all_todos')
@login_required
def all_todos():
    todos = ToDo.query.filter_by(user_id=current_user.id).all()
    return render_template('all_todos_page.html', todos=todos)

# Sign up


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        password = form.password.data
        password_confirm = form.password_confirm.data

        hashed_password = generate_password_hash(
            password, method='pbkdf2:sha256', salt_length=9)

        new_user = User(first_name=first_name, last_name=last_name,
                        email=email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)

        return redirect(url_for('home_page'))

    flash_messages = get_flashed_messages()
    return render_template('sign_up_page.html', form=form, flash_messages=flash_messages)


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

    flash_messages = get_flashed_messages()
    return render_template('login_page.html', form=form, flash_messages=flash_messages)

# Send email function


def send_email(email_sender, subject, message):
    email_receiver = environ.get('EMAIL_RECEIVER_TODO')
    password = environ.get('EMAIL_PASSWORD_TODO')

    email = EmailMessage()

    email['From'] = email_sender
    email['To'] = email_receiver
    email['Subject'] = subject
    email.set_content(message)

    context = ssl.create_default_context()

    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_receiver, password)
        smtp.sendmail(email_sender, email_receiver, email.as_string())

# Contact


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email_sender = form.email.data
        subject = form.subject.data + " - " + email_sender
        message = form.message.data

        send_email(email_sender, subject, message)

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
    app.run(debug=False)