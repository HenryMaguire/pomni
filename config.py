import os
basedir = os.path.abspath(os.path.dirname(__file__))
print(basedir)
class Config(object):
    # secret key for form validation
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    # sql database initialisaton
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    #signals app every time a change is about to be made in the db
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Setting up the email server
    os.environ['MAIL_SERVER']="mail.privateemail.com"
    os.environ["MAIL_PORT"]="587"
    os.environ["MAIL_USE_TLS"]="True"
    os.environ["MAIL_USE_SSL"] = "False"
    os.environ["MAIL_USERNAME"]="support@pomni.io"
    os.environ["MAIL_PASSWORD"]="productivity2018"

    MAIL_SERVER = os.environ.get('MAIL_SERVER')

    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 25)
    MAIL_USE_TLS = bool(os.environ.get('MAIL_USE_TLS') is not None)
    MAIL_USE_TLS = bool(os.environ.get('MAIL_PORT'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    ADMINS = ['support@pomni.io', 'henrymaguire@hotmail.co.uk']
    print( MAIL_SERVER, MAIL_PORT, MAIL_USERNAME)
