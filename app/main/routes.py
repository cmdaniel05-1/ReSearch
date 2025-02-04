from flask import render_template
import sqlalchemy as sqla


from app.main import main_blueprint as main

@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    return render_template('index.html')
