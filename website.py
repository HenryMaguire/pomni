from app import app
from app import db
from app.models import User, Project, Pomodoro

@app.shell_context_processor
def make_shell_context():
    # adds the database and models to `flask shell` environment
    return {'db': db, 'User': User, 'Project': Project, 'Pomodoro': Pomodoro}
