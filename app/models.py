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
    # will return all the 'many' posts by 'one' user
    # backref is name pointing from 'many' to 'one'
    #
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    # times indexed to enable chronological ordering
    # converted to the user's local time when displayed
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    # foreign key: references the id in user model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
