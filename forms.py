from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditorField

# WTForm

class CreateToDo(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    content = CKEditorField("Content", validators=[DataRequired()])
    priority = StringField("Priority", validators=[DataRequired()])
    submit = SubmitField("Submit ToDo")