from flask_wtf import FlaskForm
from wtforms import DecimalField, IntegerField, StringField, PasswordField, BooleanField, SubmitField, SelectField, TextAreaField
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
    description = TextAreaField('Project description', default='')
    possible_minutes = [(str(i), str(i)) for i in list(range(1,61))]
    study_length = SelectField('studylength', validators=[DataRequired()], 
                                                choices=possible_minutes, default=24)
    summary_length = SelectField('summarylength', validators=[DataRequired()], 
                                                choices=possible_minutes, default=2)
    s_break_length = SelectField('Short break length?', validators=[DataRequired()], 
                                                        choices=possible_minutes, default=4)
    l_break_length = SelectField('Long break length?', validators=[DataRequired()],
                                                        choices=possible_minutes, default=20)

    possible_repeats = [(str(i), str(i)) for i in list(range(1,15))]
    pom_num = SelectField('How many pomodoros in each block?', 
                            validators=[DataRequired()], 
                            choices=possible_repeats, default=4)
    cycle_num = SelectField('How many blocks in each session?', validators=[DataRequired()], 
                            choices=possible_repeats, default=3)

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

