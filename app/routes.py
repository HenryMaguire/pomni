from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, RegistrationForm, DeleteUserForm, NewProjectForm, DeleteProjectForm, NewPomodoroForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Project, Pomodoro
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
                                has_projects=has_projects)
    else:
        has_projects = True
        return render_template('dashboard.html',
                                projects=projects,
                                has_projects=has_projects)

@app.route("/new_project/", methods=['GET', 'POST'])
@login_required
def newProject():
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
        print 'Your project was created!'
        flash('Your project was created!')
        return redirect(url_for('dashboard'))
    else:
        return render_template('new_project.html', form=form)

@app.route("/delete_project/<title>", methods=['GET', 'POST'])
def deleteProject(title):
    form = DeleteProjectForm()
    p = Project.query.filter_by(user_id=current_user.id, title=title).first()
    if form.validate_on_submit():
        db.session.delete(p)
        db.session.commit()
        print "{}, has been deleted.".format(p.id)
        flash("{}, has been deleted.".format(p.id))
        return redirect(url_for('dashboard'))
    return render_template('delete_project.html', title='Delete project',
                            form=form, project=p)

@app.route("/project/<title>", methods=['GET', 'POST'])
@login_required
def project(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    form = NewPomodoroForm()
    if proj.current_stage == 1+3*proj.pom_num:
        proj.reset_stage()
    if proj.current_stage ==1:
        proj.num_sessions+=1
        db.session.commit()
    proj.current_stage+=1
    db.session.commit()

    if form.validate_on_submit():
        proj.current_stage-=1 # weird double counting
        db.session.commit()
        print proj.current_stage
        if proj.current_stage == 1:
            pom = Pomodoro(body = form.aim_body.data, session=proj.num_sessions, is_aim = True,
                           author=current_user, project=proj)
        else:
            pom = Pomodoro(body = form.pom_body.data,  session=proj.num_sessions,
                           is_aim = False, author=current_user, project=proj)
        pom.end_time()
        db.session.add(pom)
        return redirect(url_for("project", title=title))

    poms = Pomodoro.query.filter_by(project=proj) # print latest session
    return render_template("project.html", form=form,
                            project=proj, pomodoros=poms,
                            title=title)




@app.route("/notebank/<title>")
@login_required
def notebank(title):
    proj = Project.query.filter_by(user_id=current_user.id, title=title).first()
    poms = proj.pomodoros
    return render_template('notebank.html', project=proj, pomodoros=poms)
