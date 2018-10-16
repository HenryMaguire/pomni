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

class ResetPasswordRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Request Password Reset')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Yes, please delete my account.')

class NewProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired()])
    description = StringField('Project description', default='')
    study_length = IntegerField('Study length?', validators=[DataRequired(message="Please input how many minutes you will work for.")])
    summary_length = IntegerField('Summary length?', validators=[DataRequired()])
    s_break_length = IntegerField('Short break length?', validators=[DataRequired()])
    l_break_length = IntegerField('Long break length?', validators=[DataRequired()])

    pom_num = IntegerField('How many poms before long break?', validators=[DataRequired()])
    cycle_num = IntegerField('How many cycles?', validators=[DataRequired()])

    submit = SubmitField('Create project')

    def validate_title(self, title):

        project = Project.query.filter_by(user_id=current_user.id, title=title.data).first()
        if project is not None:
            raise ValidationError("You've already got a project with that title!")

class EditProjectForm(FlaskForm):
    title = StringField('Project title', validators=[DataRequired()])
    description = StringField('Project description')
    study_length = IntegerField('Study length')
    summary_length = IntegerField('Summary length')
    s_break_length = IntegerField('Short break length')
    l_break_length = IntegerField('Long break length')

    pom_num = IntegerField('Repetitions before long break?')
    cycle_num = IntegerField('How many cycles?')

    submit = SubmitField('Save changes')

    def __init__(self, original_title, *args, **kwargs):
        super(EditProjectForm, self).__init__(*args, **kwargs)
        self.original_title = original_title

    def validate_title(self, title):
        if title.data != self.original_title:
            project = Project.query.filter_by(title=self.title.data).first()
            if project is not None:
                raise ValidationError("You've already got a project with that title!")

class NextProjectStepForm(FlaskForm):
    end_work = SubmitField('Click to write a summary!')
    end_s_break = SubmitField("Click to get to work!")
    end_l_break = SubmitField('Click for another block!')

class DeleteProjectForm(FlaskForm):
    submit = SubmitField('Please delete this project')

class NewPomodoroForm(FlaskForm):
    aim_body = StringField('What are your aims for this session?')
    pom_body = StringField('What did you cover in this pomodoro?')

    submit = SubmitField('Enter')
