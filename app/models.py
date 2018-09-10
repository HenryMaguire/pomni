from app import db
from datetime import datetime
from flask_login import UserMixin
from app import app, login
from time import time
import jwt
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    # will return all the 'many' projects by 'one' user
    # backref is name pointing from 'many' to 'one'
    #
    projects = db.relationship('Project', backref='author', lazy='dynamic')
    pomodoros = db.relationship('Pomodoro', backref='author', lazy='dynamic')
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        #
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True)
    description = db.Column(db.String(240))
    # current_stage can be: aim, study, summary, sbreak, lbreak
    current_stage = db.Column(db.Integer, default=0)
    num_sessions = db.Column(db.Integer, default=0)
    # times indexed to enable chronological ordering
    # converted to the user's local time when displayed
    study_length = db.Column(db.Integer, default=25)
    summary_length = db.Column(db.Integer, default=2)
    s_break_length = db.Column(db.Integer, default=3)
    l_break_length = db.Column(db.Integer, default=20)
    pom_num = db.Column(db.Integer, default=3)
    cycle_num = db.Column(db.Integer, default=2)

    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # foreign key: references the id in user model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    pomodoros = db.relationship('Pomodoro', backref='project', lazy='dynamic')

    def __repr__(self):
        return '<Project {}>'.format(self.title)
    def new_session_count(self):
        self.num_sessions +=1
        db.session.commit()
    def step_stage(self):
        self.current_stage +=1
        db.session.commit()
    def reset_stage(self):
        self.current_stage = 0
        db.session.commit()

class Pomodoro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session = db.Column(db.Integer) # groups aim/poms in same session together
    body = db.Column(db.String(420))
    is_aim = db.Column(db.Boolean)
    # times indexed to enable chronological ordering
    # converted to the user's local time when displayed
    timestamp_start = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    timestamp_end = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # foreign key: references the id in user model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    def __repr__(self):
        return '<Pomodoro {}>'.format(self.id)
    def end_time(self):
        self.timestamp_end = datetime.utcnow()
        db.session.commit()

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
