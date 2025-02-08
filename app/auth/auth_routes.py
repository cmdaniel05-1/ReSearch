from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.auth import auth_blueprint as auth
from app.auth.auth_forms import StudentRegistrationForm, FacultyRegistrationForm, LoginForm
from app.main.models import Student, Faculty
import sqlalchemy as sqla


@auth.route('/faculty-register', methods=['GET', 'POST'])
def faculty_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = FacultyRegistrationForm()
    if rform.validate_on_submit():
        faculty = Faculty(wpi_id = rform.wpi_id.data,
                            username = rform.username.data,
                            firstname = rform.firstname.data,
                            lastname = rform.lastname.data,
                            email = rform.email.data,
                            phone_num = rform.phone_num.data)
        faculty.set_password(rform.password.data)
        db.session.add(faculty)
        db.session.commit()
        flash('Congratulations, you are now a registered faculty user!')
        return redirect(url_for('main.index'))
    return render_template('faculty-register.html', form = rform)

@auth.route('/student-register', methods=['GET', 'POST'])
def student_register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    rform = StudentRegistrationForm()
    if rform.validate_on_submit():
        student = Student(wpi_id = rform.wpi_id.data,
                            username = rform.username.data,
                            firstname = rform.firstname.data,
                            lastname = rform.lastname.data,
                            email = rform.email.data)
        student.set_password(rform.password.data)
        db.session.add(student)
        db.session.commit()
        flash('Congratulations, you are now a registered student user!')
        return redirect(url_for('main.index'))
    return render_template('student-register.html', form = rform)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(Student).where(Student.username == lform.username.data)
        user = db.session.scalars(query).first()
        isStudent = True
        if(user is None):
            isStudent = False
            query = sqla.select(Faculty).where(Faculty.username == lform.username.data)
            user = db.session.scalars(query).first()
        if (user is None) or (user.check_password(lform.password.data) == False):
            return redirect(url_for('auth.login'))
        login_user(user, isStudent, remember=lform.remember_me.data)
        flash('The user {} has succesfully logged in! {}'.format(current_user.username, current_user.is_authenticated))
        return redirect(url_for('main.index'))
    return render_template('login.html', form = lform)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))