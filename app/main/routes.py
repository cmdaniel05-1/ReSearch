from flask import render_template
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app.main import main_blueprint as main
from app.main.models import Position
from app import db

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    positions = db.session.query(Position)
    return render_template('index.html', positions = positions)
