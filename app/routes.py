from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, DeleteUserForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User
import time

@app.route("/", methods=['GET', 'POST'])
@app.route("/login/", methods=['GET', 'POST'])
@app.route("/home/", methods=['GET', 'POST'])

def login():
    if current_user.is_authenticated:
        # if they're logged in already go to dash
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        # take username and query database with it
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            print 'Invalid username or password'
            flash('Invalid username or password')
            return redirect(url_for('login'))
        else:
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('dashboard'))
    return render_template('login.html', title='Sign In', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        # if they're logged in already go to dash
        print current_user
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # take username and query database with it
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print 'Congratulations, you are now registered!'
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/delete_user", methods=['GET', 'POST'])
def deleteUser():
    form = DeleteUserForm()
    if form.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        print "{}, we're sorry to see you go!".format(current_user.username)
        flash("{}, we're sorry to see you go!".format(current_user.username))
        import time
        return redirect(url_for('login'))
    return render_template('delete_user.html', title='Delete account', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/project/", methods=['GET', 'POST'])
@login_required
def project():
    return render_template('project.html')

@app.route("/dashboard/", methods=['GET', 'POST'])
@login_required
def dashboard():
    projects = [
        {
            'title': "Project 1",
            'stampLast': '31:08:2018 13:00',
            'postLast': 'Just added a new feature!'
        },
        {
            'title': "Project 2",
            'stampLast': '31:08:2018 14:00',
            'postLast': 'Just added a cool feature!',
        }
    ]
    return render_template('dashboard.html', projects=projects)

@app.route("/notebank/")
@login_required
def notebank():
    return render_template('notebank.html')
