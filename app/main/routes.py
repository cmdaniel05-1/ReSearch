from flask import render_template, redirect, flash, url_for
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app import db
from app.main.forms import PostForm, FieldForm, LanguageForm
from app.main.models import Position, Field, Language
from app.main import main_blueprint as main
from app.main.models import Position
from flask_login import current_user


@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
def index():
    positions = db.session.query(Position).options(db.joinedload(Position.faculty)).all() #patched bug with lazy loading - do not remove
    return render_template('index.html', positions = positions)

@main.route('/create/position', methods=['GET', 'POST'])
def create():
    form = PostForm()
    if form.validate_on_submit():
        new_position = Position(faculty_id = current_user.id,
                                title = form.title.data,
                                description = form.description.data,
                                start_date = form.start_date.data,
                                end_date = form.end_date.data,
                                req_time = form.req_time.data,
                                student_count = form.student_count.data)
        for f in form.fields.data:
            new_position.fields.append(f)
        for l in form.languages.data:
            new_position.languages.append(l)
        db.session.add(new_position)
        db.session.commit()
        flash('"' + new_position.title + '" has been posted.')
        return redirect(url_for('main.index'))
    return render_template('create.html', form = form)

@main.route('/create/field', methods=['GET', 'POST'])
def field():
    form = FieldForm()
    if form.validate_on_submit():
        new_field = Field(name = form.name.data)
        db.session.add(new_field)
        db.session.commit()
        return redirect(url_for('main.create'))
    return render_template('field.html', form = form)

@main.route('/create/language', methods=['GET', 'POST'])
def language():
    form = LanguageForm()
    if form.validate_on_submit():
        new_language = Language(name = form.name.data)
        db.session.add(new_language)
        db.session.commit()
        return redirect(url_for('main.create'))
    return render_template('language.html', form = form)