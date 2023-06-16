from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import DataRequired, URL, Email
from flask_ckeditor import CKEditorField

# WTForms

class CreateToDo(FlaskForm):
    priority = SelectField("Priority", choices=[("must", "Must ToDo"), ("secondary", "Secondary ToDo"), ("optional", "Optional ToDo")], validators=[DataRequired()])
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    submit = SubmitField("Confirm")
    
class RegisterForm(FlaskForm):
    first_name = StringField("First Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    checkbox = BooleanField("Agree to Terms and Conditions", validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")
    
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Let Me In!")
    

class ContactForm(FlaskForm):
    first_name = StringField("Name", validators=[DataRequired()])
    last_name = StringField("Last Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = CKEditorField("Message", validators=[DataRequired()])
    submit = SubmitField("Send Message")