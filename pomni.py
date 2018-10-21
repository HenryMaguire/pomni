from app import app
from app import db
from app.models import User, Project, Pomodoro
from sqlalchemy import desc
from datetime import datetime

@app.shell_context_processor
def make_shell_context():
    # adds the database and models to `flask shell` environment
    projects = Project.query.filter_by().all()
    for p in projects:
        poms = Pomodoro.query.filter_by(project=p)
        latest_pom = poms.order_by(desc(Pomodoro.timestamp_end)).first()
        try:
            p.last_timestamp = latest_pom.timestamp_end
            db.session.add(p)
            db.session.commit()
        except:
            p.last_timestamp = datetime.utcnow()
            print (p.title, " no timestamp, so set to now")
            db.session.add(p)
            db.session.commit()
            pass
    return {'db': db, 'User': User, 'Project': Project, 'Pomodoro': Pomodoro}

