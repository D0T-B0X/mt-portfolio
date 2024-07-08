from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired
from flask_ckeditor import CKEditorField


class Project(FlaskForm):
    name = StringField('Name of the Project', validators=[DataRequired()])
    description = StringField('Short Description of the Project', validators=[DataRequired()])
    link_name = StringField("Enter the name of the link", validators=[DataRequired()])
    link_path = StringField("Enter the path to the link", validators=[DataRequired()])
    content = CKEditorField("Project details", validators=[(DataRequired())])
    file = FileField("Upload Files")
    submit = SubmitField("Add Project")


class Edit(FlaskForm):
    name = StringField('Name of the Project', validators=[DataRequired()])
    description = StringField('Short Description of the Project', validators=[DataRequired()])
    link_name = StringField("Enter the name of the link", validators=[DataRequired()])
    link_path = StringField("Enter the path to the link", validators=[DataRequired()])
    content = CKEditorField("Project details", validators=[(DataRequired())])
    file = FileField("Upload Files")
    submit = SubmitField("Done")


class Login(FlaskForm):
    password = PasswordField("Enter your Password:", validators=[DataRequired()])
    submit = SubmitField("Login")