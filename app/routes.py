from flask import render_template, flash, redirect, url_for, get_flashed_messages, jsonify, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DeleteUserForm, NewProjectForm
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.forms import DeleteProjectForm, NewPomodoroForm, NextProjectStepForm, EditProjectForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Pomodoro
from datetime import datetime
from sqlalchemy import desc


@app.route("/_new_pomodoro", methods=['POST'])
def new_pomodoro():
    return jsonify({"hello" : "there"})

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
            print('Invalid username or password')
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
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # take username and query database with it
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        print('Congratulations, you are now registered!')
        flash('Congratulations, you are now registered!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash('Check your email for the instructions to reset your password')
        return redirect(url_for('login'))
    return render_template('reset_password_request.html',
                           title='Reset Password', form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been changed.')
        return redirect(url_for('login'))
    return render_template('reset_password.html',
                           title='Reset Password', form=form)

@app.route("/delete_user", methods=['GET', 'POST'])
def deleteUser():
    form = DeleteUserForm()
    if form.validate_on_submit():
        db.session.delete(current_user)
        db.session.commit()
        print ("{}, we're sorry to see you go!".format(current_user.username))
        flash("{}, we're sorry to see you go!".format(current_user.username))
        return redirect(url_for('login'))
    return render_template('delete_user.html', title='Delete account', form=form)

@app.route('/user_settings')
def userSettings():
    return render_template('user_settings.html', user=current_user)

@app.route('/logout')
def logout():
    logout_user()
    flash("See you again soon!")
    return redirect(url_for('login'))

@app.route("/dashboard/", methods=['GET', 'POST'])
@login_required
def dashboard():
    # If the user has no projects, suggest making a new one
    project0 = Project.query.filter_by(user_id=current_user.id).first()
    projects = Project.query.filter_by(user_id=current_user.id)
    if project0 is None:
        has_projects = False
        return render_template('dashboard.html',
                                projects=projects,
                                has_projects=has_projects, title='Dashboard')
    else:
        has_projects = True
        return render_template('dashboard.html',
                                projects=projects,
                                has_projects=has_projects, title='Dashboard')

@app.route("/new_project/", methods=['GET', 'POST'])
@login_required
def newProject():
    #app.logger.error('This is a error log test')
    form = NewProjectForm()
    if form.validate_on_submit():
        # take username and query database with it
        project = Project(title=form.title.data, description=form.description.data,
                       study_length=form.study_length.data,
                       summary_length=form.summary_length.data,
                       s_break_length=form.s_break_length.data,
                       l_break_length=form.l_break_length.data,
                       pom_num=form.pom_num.data,
                       cycle_num=form.cycle_num.data,
                       author=current_user)
        db.session.add(project)
        db.session.commit()
        print( 'Your project was created!')
        flash('Your project was created!')
        return redirect(url_for('dashboard'))
    else:
        return render_template('new_project.html', form=form, title='Project creation')

@app.route("/delete_project/<title>", methods=['GET', 'POST'])
def deleteProject(title):
    form = DeleteProjectForm()
    p = Project.query.filter_by(user_id=current_user.id, title=title).first()
    if form.validate_on_submit():
        db.session.delete(p)
        db.session.commit()
        print ("{}, has been deleted.".format(p.id))
        flash("{}, has been deleted.".format(p.id))
        return redirect(url_for('dashboard'))
    return render_template('delete_project.html', title='Delete project',
                            form=form, project=p)

@app.route("/project/<title>", methods=['GET', 'POST'])
@login_required
def project(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    form = NewPomodoroForm()
    step_form = NextProjectStepForm()
    if proj.current_stage > 3*proj.pom_num:
        proj.reset_stage()

    if form.validate_on_submit():
        #proj.current_stage-=1 # weird double counting
        #db.session.commit()
        pom = 0
        print (proj.current_stage)
        if proj.current_stage == 0:
            proj.num_sessions+=1
            db.session.commit()

            pom = Pomodoro(body = form.aim_body.data, session=proj.num_sessions, is_aim = True,
                           author=current_user, project=proj, timestamp_end = datetime.utcnow())
            proj.current_stage+=1
            db.session.commit()
            db.session.add(pom)
            db.session.commit()
            return redirect(url_for("project", title=title))
    poms = Pomodoro.query.filter_by(project=proj) # print latest session
    current_aim =  Pomodoro.query.filter_by(project=proj,
                                            session=proj.num_sessions,
                                            is_aim=True).first()
    most_recent = None
    try:
        recent_first = poms.order_by(desc(Pomodoro.timestamp_end)).all()
        recent_first_non_blank = [i for i in recent_first if len(i.body)>0]
        if len(recent_first_non_blank)>0:
            most_recent = recent_first_non_blank[0]
    except Exception as err:
        print (err)
    return render_template("project.html", step_form=step_form, form=form,
                            project=proj, pomodoros=poms,
                            title=title, recents = [current_aim, most_recent])

def project(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    form = NewPomodoroForm()
    step_form = NextProjectStepForm()
    if proj.current_stage > 3*proj.pom_num:
        proj.reset_stage()

    if form.validate_on_submit():
        #proj.current_stage-=1 # weird double counting
        #db.session.commit()
        pom = 0
        print (proj.current_stage)
        if proj.current_stage == 0:
            proj.num_sessions+=1
            db.session.commit()

            pom = Pomodoro(body = form.aim_body.data, session=proj.num_sessions, is_aim = True,
                           author=current_user, project=proj, timestamp_end = datetime.utcnow())
            proj.current_stage+=1
            db.session.commit()
            db.session.add(pom)
            db.session.commit()
            return redirect(url_for("project", title=title))
        else:
            pom = Pomodoro(body = form.pom_body.data,  session=proj.num_sessions,
                           is_aim = False, author=current_user, project=proj)
            proj.current_stage+=1
            db.session.commit()
            pom.end_time()
            db.session.add(pom)
            db.session.commit()
            return redirect(url_for("project", title=title))
    if step_form.validate_on_submit():
        proj.current_stage+=1
        db.session.commit()
        return redirect(url_for("project", title=title))
    poms = Pomodoro.query.filter_by(project=proj) # print latest session
    current_aim =  Pomodoro.query.filter_by(project=proj,
                                            session=proj.num_sessions,
                                            is_aim=True).first()
    most_recent = None
    try:
        recent_first = poms.order_by(desc(Pomodoro.timestamp_end)).all()
        recent_first_non_blank = [i for i in recent_first if len(i.body)>0]
        if len(recent_first_non_blank)>0:
            most_recent = recent_first_non_blank[0]
    except Exception as err:
        print (err)
    return render_template("project.html", step_form=step_form, form=form,
                            project=proj, pomodoros=poms,
                            title=title, recents = [current_aim, most_recent])

@app.route("/edit_project/<title>", methods=['GET', 'POST'])
@login_required
def editProject(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    form = EditProjectForm(proj.title)
    if form.validate_on_submit():
        # take username and query database with it
        proj.title=form.title.data
        proj.description=form.description.data
        proj.study_length=form.study_length.data
        proj.summary_length=form.summary_length.data
        proj.s_break_length=form.s_break_length.data
        proj.l_break_length=form.l_break_length.data
        proj.pom_num=form.pom_num.data
        proj.cycle_num=form.cycle_num.data

        db.session.commit()
        print( 'Your project has been edited!')
        flash('Your project has been edited!')
        return redirect(url_for('project', title=proj.title))
    else:
        return render_template('edit_project.html', form=form, project=proj,
                                                        title='Edit project')


@app.route("/notebank/<title>")
@login_required
def notebank(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    poms = proj.pomodoros
    return render_template('notebank.html', project=proj, pomodoros=poms, title=proj.title)
