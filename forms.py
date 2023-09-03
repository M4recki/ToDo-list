from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, RadioField, ValidationError
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

# WTForms


class CreateToDo(FlaskForm):
    priority = SelectField("Select priority of your ToDo", choices=[("must", "Must ToDo"), ("secondary", "Secondary ToDo"), ("optional", "Optional ToDo")], validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Confirm")
    
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password_confirm = PasswordField('Confirm Password', validators=[DataRequired()])
    checkbox = BooleanField("Agree to Terms and Conditions", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")
    
    def validate_email(self, field):
        from app import app
        from models import User
        with app.app_context():
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email already exists. Please login or use a different email.')

    def validate_password_confirm(self, field):
        if field.data != self.password.data:
            raise ValidationError("Passwords do not match. Please try again.")
        
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
    

class ContactForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    subject = StringField("Subject", validators=[DataRequired()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")