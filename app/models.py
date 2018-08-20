from app import db
from datetime import datetime
from flask_login import UserMixin
from app import login

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

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), index=True, unique=True)
    description = db.Column(db.String(240))
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

    def __repr__(self):
        return '<Project {}>'.format(self.title)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
