from flask import render_template, redirect, flash, url_for, request
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app import db
from app.main.forms import PostForm, FieldForm, LanguageForm, FacultyEditForm
from app.main.models import Position, Field, Language
from app.main import main_blueprint as main
from app.main.models import Position, Faculty
from flask_login import current_user, login_required


@main.route('/', methods=['GET'])
@main.route('/index', methods=['GET'])
@login_required
def index():
    positions = db.session.query(Position).options(db.joinedload(Position.faculty)).all() #patched bug with lazy loading - do not remove
    return render_template('index.html', positions = positions)

@main.route('/create/position', methods=['GET', 'POST'])
@login_required
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
@login_required
def field():
    form = FieldForm()
    if form.validate_on_submit():
        new_field = Field(name = form.name.data)
        db.session.add(new_field)
        db.session.commit()
        return redirect(url_for('main.create'))
    return render_template('field.html', form = form)

@main.route('/create/language', methods=['GET', 'POST'])
@login_required
def language():
    form = LanguageForm()
    if form.validate_on_submit():
        new_language = Language(name = form.name.data)
        db.session.add(new_language)
        db.session.commit()
        return redirect(url_for('main.create'))
    return render_template('language.html', form = form)

@main.route('/profile/faculty', methods=['GET'])
@login_required
def faculty_profile():
    faculty = db.session.scalars(sqla.select(Faculty).where(Faculty.id == current_user.id)).first()
    print(faculty.phone_num)
    return render_template('display_faculty.html', faculty = faculty)

@main.route('/edit/faculty', methods=['GET', 'POST'])
@login_required
def faculty_edit():
    form = FacultyEditForm()
    if request.method == 'POST':
        current_user.wpi_id = form.wpi_id.data
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone_num = form.phone_num.data
        current_user.set_password(form.password.data)
        db.session.add(current_user)
        db.session.commit()
        return redirect(url_for('main.faculty_profile'))
    elif request.method == 'GET':
        form.wpi_id.data = current_user.wpi_id
        form.username.data = current_user.username
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone_num.data = current_user.phone_num
    else:
        pass
    return render_template('edit_faculty.html', title = 'Edit Profile', form = form)