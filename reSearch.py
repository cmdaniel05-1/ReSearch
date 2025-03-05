from datetime import datetime, timezone
from flask_login import current_user
from app import create_app, db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo
from app.main.models import Language, Position, Student, Faculty, User
from config import Config
import json
from os import environ as env

app = create_app(Config)

@app.shell_context_processor
def make_shell_context():
    return {'sqla': sqla, 'sqlo': sqlo, 'Position': Position, 'Language': Language, 'Student': Student, 'Faculty': Faculty}

@app.context_processor
def inject_user_type():
    return {
        "is_faculty": current_user.is_authenticated and current_user.type == 'Faculty',
        "is_student": current_user.is_authenticated and current_user.type == 'Student'
    }
    
@app.before_request
def initDB(*args, **kwargs):
    if app._got_first_request:
        db.create_all()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=env.get("PORT", 3000))