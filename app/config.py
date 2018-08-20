import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    # secret key for form validation
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # sql database initialisaton
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    #signals app every time a change is about to be made in the db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
