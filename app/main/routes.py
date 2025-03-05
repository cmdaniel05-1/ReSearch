from flask import render_template, redirect, flash, url_for, request, jsonify
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from app import db
from app.main.forms import AddFieldForm, AddLanguageForm, DeleteFieldForm, DeleteLanguageForm, PostForm, FacultyEditForm, StudentEditForm, EmptyForm, ApplicationForm, UpdateAppStatusForm, UpdateRefStatusForm
from app.main.models import Application, Position, Field, Language, Student, Faculty
from app.main import main_blueprint as main
from app.main.models import Position
from flask_login import current_user, login_required


@main.route('/', methods=['GET','POST'])
@main.route('/index', methods=['GET','POST'])
@login_required
def index():
    empty_form = EmptyForm()
    application_form = ApplicationForm()
    faculty = db.session.query(Faculty).all()
    application_form.reference.choices = [(f.id, f.firstname + ' ' + f.lastname + ' - ' + f.email) for f in faculty]
    if current_user.type == "faculty":
        positions = db.session.query(Position).filter_by(faculty_id = current_user.id).options(db.joinedload(Position.faculty)).all() #patched bug with lazy loading - do not remove
    else:
        positions = db.session.query(Position).options(db.joinedload(Position.faculty)).all() #patched bug with lazy loading - do not remove
    return render_template('index.html', positions=positions, empty_form=empty_form, application_form=application_form)

@main.route('/position/creation', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.type == 'student':
        return redirect(url_for('main.index'))
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

@main.route('/field/edit', methods=['GET', 'POST'])
@login_required
def field():
    if current_user.type == 'student':
        return redirect(url_for('main.index'))
    createform = AddFieldForm()
    if 'create_field' in request.form and createform.validate_on_submit():
        if createform.name.data:
            new_field = Field(name = createform.name.data)
            db.session.add(new_field)
        db.session.commit()
        return redirect(url_for('main.create'))
    
    deleteform = DeleteFieldForm()
    if 'delete_field' in request.form and deleteform.validate_on_submit():
        for f in deleteform.fields.data:
            db.session.delete(f)
        db.session.commit()
        return redirect(url_for('main.create'))
    fields = Field.query.all()
    return render_template('field.html', createform = createform, deleteform = deleteform, fields = fields)


@main.route('/language/edit', methods=['GET', 'POST'])
@login_required
def language():
    if current_user.type == 'student':
        return redirect(url_for('main.index'))
    createform = AddLanguageForm()
    if 'create_language' in request.form and createform.validate_on_submit():
        if createform.name.data:
            new_language = Language(name = createform.name.data)
            db.session.add(new_language)
        db.session.commit()
        return redirect(url_for('main.create'))
    
    deleteform = DeleteLanguageForm()
    if 'delete_language' in request.form and deleteform.validate_on_submit():
        for l in deleteform.languages.data:
            db.session.delete(l)
        db.session.commit()
        return redirect(url_for('main.create'))
    languages = Language.query.all()
    return render_template('language.html', createform = createform, deleteform = deleteform, languages = languages)

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    if current_user.type == "faculty":
        request_apps = Application.query.filter(Application.reference_id == current_user.id).all()
        form = UpdateRefStatusForm()
        return render_template('display_profile.html', title = 'Profile', user = current_user, request_apps = request_apps, form = form)
    return render_template('display_profile.html', title = 'Profile', user = current_user)

@main.route('/profile/<username>', methods=['GET'])
@login_required
def profile_id(username):
    if current_user.type == "student":
        flash("You do not have permission to access to {}'s profile".format(username))
        return render_template('display_profile.html', title = 'Profile', user = current_user)
    elif current_user.type == "faculty":
        user = Student.query.filter(Student.username == username).first()
        if user is None:
            flash('User not found')
            return redirect(url_for('main.index'))

        return render_template('display_profile.html', title = 'Profile', user = user)



@main.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    if current_user.type == 'faculty':
        form = FacultyEditForm()
    else:
        form = StudentEditForm()
    if form.validate_on_submit():
        current_user.wpi_id = form.wpi_id.data
        current_user.username = form.username.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone_num = form.phone_num.data
        if current_user.type == 'student':
            current_user.major = form.major.data
            current_user.gpa = form.gpa.data
            current_user.grad_date = form.grad_date.data
            current_user.fields = form.fields.data
            current_user.languages = form.languages.data
        if form.password2.data:
            current_user.set_password(form.password2.data)
        db.session.add(current_user)
        db.session.commit()
        flash('Profile updated successfully!')
        return redirect(url_for('main.profile'))
    else:
        form.wpi_id.data = current_user.wpi_id
        form.username.data = current_user.username
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone_num.data = current_user.phone_num
        if current_user.type == 'student':
            form.major.data = current_user.major
            form.gpa.data = current_user.gpa
            form.grad_date.data = current_user.grad_date
            form.fields.data = current_user.fields
            form.languages.data = current_user.languages
    return render_template('edit_profile.html', title = 'Edit Profile', form = form)

@main.route('/application/<position_id>/submission', methods=['POST'])
@login_required
def apply(position_id):
    if current_user.type == 'faculty':
        return redirect(url_for('main.index'))
    
    theposition = db.session.get(Position, position_id)
        
    if theposition is None:
        flash('No such position exists')
        return redirect(url_for('main.index'))
    
    # Access the form data directly from the request
    form = ApplicationForm(request.form)
    faculty = db.session.query(Faculty).all()
    form.reference.choices = [(f.id, f.firstname + ' ' + f.lastname + ' - ' + f.email) for f in faculty]

    if form.validate_on_submit():
        reference = Faculty.query.filter(Faculty.id == form.reference.data).first()
        
        if reference.id == theposition.faculty_id:
            flash('Reference cannot be the position author')
            return redirect(url_for('main.index'))

        current_user.apply(theposition, reference, form.statement.data)
        flash('You have applied to {}.'.format(theposition.title))
        return redirect(url_for('main.index'))
    
    for field, errors in form.errors.items():
            for error in errors:
                flash(f'Error in {field}: {error}')
    
    return redirect(url_for('main.index')) 


@main.route('/application/<position_id>/withdrawal', methods=['GET','POST'])
@login_required
def withdraw(position_id):
    if current_user.type == 'faculty':
        return redirect(url_for('main.index'))
    theposition = db.session.get(Position, position_id)
    if theposition is None:
        flash('No such position exists')
        return redirect(request.referrer)
    current_user.withdraw(theposition)
    db.session.commit()
    theposition = db.session.get(Position, position_id)
    data = {
        'position_id': theposition.id
    }
    return jsonify(data)

@main.route('/applications/application/<position_id>/withdrawal', methods=['GET','POST'])
@login_required
def applications_withdraw(position_id):
    if current_user.type == 'faculty':
        return redirect(url_for('main.index'))
    theposition = db.session.get(Position, position_id)
    if theposition is None:
        flash('No such position exists')
        return redirect(request.referrer)
    current_user.withdraw(theposition)
    db.session.commit()
    flash('You have withdrawn from {}'.format(theposition.title))
    return redirect(request.referrer)
    

@main.route('/applications/<student_id>/view', methods=['GET'])
@login_required
def view_applications(student_id):
    if current_user.type == 'faculty':
        return redirect(url_for('main.index'))
    student = db.session.get(Student, student_id)
    form = EmptyForm()
    return render_template('applications.html', title = 'Applications', form = form)


@main.route('/application/<position_id>/<student_id>/view', methods=['GET'])
@login_required
def view_application(position_id, student_id):
    if current_user.type == "student":
        return redirect(url_for('main.index'))
    form = UpdateAppStatusForm()
    application = db.session.query(Application).filter(
            Application.position_id == position_id,
            Application.student_id == student_id
        ).first() 
    if application == None:
        flash("This application does not exist")
        return redirect(url_for('main.index'))
    
    return render_template('application.html', application = application, form = form, is_available = application.student_applied.is_available())

@main.route('/application/<position_id>/<student_id>/update',  methods = ['POST'])
@login_required
def update_app_status(position_id, student_id):
    if current_user.type == "student":
        return redirect(url_for('main.index'))
    position = db.session.query(Position).filter(Position.id == position_id).first()
    approved = db.session.query(Application).filter(Application.position_id == position_id, Application.app_is_accepted).count()
    application = db.session.query(Application).filter(
            Application.position_id == position_id,
            Application.student_id == student_id
        ).first() 
    if application == None:
        flash("This application does not exist")
        return redirect(url_for('main.index'))
    form = UpdateAppStatusForm(request.form)
    if form.validate_on_submit():
        if application.app_is_accepted:
            if form.status.data == "Approve":
                if approved >= position.student_count:
                    flash("You have already approved the maximum amount of students.")
                else:
                    application.app_is_accepted = True
                    db.session.add(application)
                    db.session.commit()
                    flash("Application status successfully updated")
            elif form.status.data == "Pending":
                application.app_is_accepted = None
                db.session.add(application)
                db.session.commit()
                flash("Application status successfully updated")
            else:
                application.app_is_accepted = False
                db.session.add(application)
                db.session.commit()
                flash("Application status successfully updated")
        else:
            if form.status.data == "Approve":
                if approved >= position.student_count:
                    flash("You have already approved the maximum amount of students.")
                else:
                    application.app_is_accepted = True
                    db.session.add(application)
                    db.session.commit()
                    flash("Application status successfully updated")
            elif form.status.data == "Pending":
                application.app_is_accepted = None
                db.session.add(application)
                db.session.commit()
                flash("Application status successfully updated")
            else:
                application.app_is_accepted = False
                db.session.add(application)
                db.session.commit()
                flash("Application status successfully updated")
    else:
        flash("Application status not updated, please check form input")
    return redirect(url_for("main.view_application", position_id = position_id, student_id = student_id))


@main.route('/application/<position_id>/<student_id>/updateref',  methods = ['POST'])
@login_required
def update_ref_status(position_id, student_id):
    if current_user.type == "student":
        return redirect(url_for('main.index'))
    
    application = db.session.query(Application).filter(
            Application.position_id == position_id,
            Application.student_id == student_id
        ).first() 
    if application == None:
        flash("This application does not exist")
        return redirect(url_for('main.index'))
    form = UpdateRefStatusForm(request.form)
    if form.validate_on_submit():
        if form.status.data == "Approve":
            application.ref_is_accepted = True
        else:
            application.ref_is_accepted = False
        db.session.add(application)
        db.session.commit()
        flash("Reference status successfully updated")
    else:
        flash("Reference status not updated, please check form input")
    return redirect(url_for("main.profile"))