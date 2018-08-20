from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from flask_login import current_user
from app.models import User, Project


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('That username is already taken.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Please delete my account')

class NewProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired()])
    description = StringField('Project description')
    study_length = IntegerField('Study length?')
    summary_length = IntegerField('Summary length?')
    s_break_length = IntegerField('Short break length?')
    l_break_length = IntegerField('Long break length?')

    pom_num = IntegerField('How many poms before long break?')
    cycle_num = IntegerField('How many cycles?')

    submit = SubmitField('Create project')

    def validate_title(self, title):
        project = Project.query.filter_by(title=title.data).first()
        if project is not None:
            raise ValidationError("You've already got a project with that title!")
