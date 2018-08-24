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
    description = StringField('Project description', default='')
    study_length = IntegerField('Study length?', default=25)
    summary_length = IntegerField('Summary length?', default=2)
    s_break_length = IntegerField('Short break length?', default=3)
    l_break_length = IntegerField('Long break length?', default=25)

    pom_num = IntegerField('How many poms before long break?', default=4)
    cycle_num = IntegerField('How many cycles?', default=2 )

    submit = SubmitField('Create project')

    def validate_title(self, title):

        project = Project.query.filter_by(user_id=current_user.id, title=title.data).first()
        if project is not None:
            raise ValidationError("You've already got a project with that title!")

class DeleteProjectForm(FlaskForm):
    submit = SubmitField('Please delete this project')

class NewPomodoroForm(FlaskForm):
    aim_body = StringField('What are your aims for this session?')
    pom_body = StringField('What did you cover in this pomodoro?',
                            validators=[DataRequired()])

    submit = SubmitField('Enter')
