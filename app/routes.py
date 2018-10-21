from flask import render_template, flash, redirect, url_for, get_flashed_messages, jsonify, request
from app import app, db
from app.forms import LoginForm, RegistrationForm, DeleteUserForm
from app.forms import ResetPasswordRequestForm, ResetPasswordForm
from app.forms import DeleteProjectForm, NewProjectForm, EditProjectForm
from app.email import send_password_reset_email
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Pomodoro
from datetime import datetime
from sqlalchemy import desc

@app.route("/_reset_session/<title>", methods=['GET','POST'])
def reset_session(title):
    print()
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    proj.current_stage =-1
    db.session.add(proj)
    db.session.commit()
    return redirect(url_for('project', title=title))

@app.route("/_get_response_json/<title>/<stage>/<pom_num>", methods=['GET','POST'])
def get_response_json(stage, pom_num, title):
    stage, pom_num = int(stage), int(pom_num)
    time_dict = request.form
    current_aim, last_summary = get_recent_activity(title)
    
    if len(request.form)==0:
        proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
        time_dict = {'lbt' : str(proj.l_break_length), 'st' : str(proj.summary_length), 
                    'wt' : str(proj.study_length), 'sbt' : str(proj.s_break_length)}
    
    response_dict = {"stage" : stage, "header": "What are your aims for this session?",
                        "button" : "Submit", "show_timer" : True, 
                        "show_form" : True, "time": time_dict['st'], 
                        "current_aim" : current_aim, "last_summary": last_summary}
    if (stage==-1) or stage >(3*pom_num):
        # let's begin
        stage = -1
        proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
        proj.current_stage =-1
        proj.num_sessions+=1
        db.session.add(proj)
        db.session.commit()
        response_dict.update({"header": "Are you ready to begin?",
                        "button" : "Begin", "show_form" : False, 
                        "time": str(0), "show_timer": False})
    elif ((stage==0) and (stage < (3*pom_num))):
        # Aim time 
        response_dict = response_dict # defaults are for aim
    elif (((stage-1)%3==0) and (stage < (3*pom_num))):
        # work time
        response_dict.update({"header": "Get to work!", "button" : "Skip", 
                            "show_form" : False, "time": time_dict['wt']})
    elif ((stage-2)%3==0) and (stage < (3*pom_num)):
        # summary time 
        response_dict.update({"header": "Summarise what you just did.", "time": time_dict['st']})
    elif ((stage-3)%3==0) and (stage < (3*pom_num)):
        # short break time
        response_dict.update({"header": "Take a short break.",
                        "button" : "Skip", "show_form" : False, "time": time_dict['sbt']})
    elif stage == (3*pom_num):
        # long break time
        response_dict.update({"header": "Good job! Take a long break.",
                        "button" : "Skip", "show_form" : False, 
                        "time": time_dict['lbt']})
    else:
        raise Exception("Gone outside of the allowed stage values in the timer app")
        pass # this should never be the case.
    return jsonify(response_dict)

from dateutil.tz import gettz

@app.route("/_next_stage/<title>", methods=['GET','POST'])
def increment_stage(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    proj.current_stage+=1
    db.session.add(proj)
    db.session.commit()
    return get_response_json(proj.current_stage, proj.pom_num, proj.title)

@app.route("/_new_pomodoro", methods=['POST'])
def new_pomodoro():
    rf = request.form
    body = rf['summary'].rstrip() # Remove trailing newline
    
    timestamp = datetime.now()
    project_title = rf['title']
    stage = int(rf['stage'])
    pom_num = int(rf['pn'])
    is_aim = False
    if stage == 0 :
        is_aim = True
    print("UPDATING DB")
    proj = Project.query.filter_by(user_id=current_user.id, title=project_title).first()
    pom = Pomodoro(body = body, session=proj.num_sessions, is_aim = is_aim,
                           author=current_user, project=proj, timestamp_end = timestamp)
    db.session.add(pom)
    proj.current_stage+=1
    proj.last_timestamp = datetime.utcnow()
    db.session.add(proj)
    db.session.commit()
    
    return get_response_json(proj.current_stage, pom_num, proj.title)


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
    form = NewProjectForm(None)
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

def get_recent_activity(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    poms = Pomodoro.query.filter_by(project=proj, is_aim=False) # print latest session
    current_aim =  Pomodoro.query.filter_by(project=proj,
                                            session=proj.num_sessions,
                                            is_aim=True).first()
    most_recent_body = ""
    current_aim_body = ""
    try:
        recent_first = poms.order_by(desc(Pomodoro.timestamp_end)).all()
        recent_first_non_blank = [i for i in recent_first if len(i.body)>0]
        if len(recent_first_non_blank)>0:
            most_recent = recent_first_non_blank[0]
        try:
            current_aim_body = current_aim.body
        except:
            pass
        try:
            most_recent_body = most_recent.body
        except:
            pass
    except Exception as err:
        print (err)
    return  current_aim_body, most_recent_body
    

@app.route("/project/<title>", methods=['GET', 'POST'])
@login_required
def project(title):
    max_summary_length = 440
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    parameters=[proj.study_length, proj.summary_length, proj.s_break_length, 
    proj.l_break_length, proj.pom_num, proj.cycle_num]
    stage, pom_num = proj.current_stage, proj.pom_num
    return render_template("project.html", project=proj, title=title, 
                            parameters=parameters, max_summary_length=max_summary_length)

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
