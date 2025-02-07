from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.auth import auth_blueprint as auth
from app.auth.auth_forms import RegistrationForm, LoginForm
from app.main.models import Student
import sqlalchemy as sqla


@auth.route('/login', methods = ['GET', 'POST' ])
def login():
    lform = LoginForm()
    if lform. validate_on_submit():
        query = sqla.select(Student).where(Student.username == lform.username.data)
        student = db. session.scalars(query).first()
        if (student is None) or (student.check_password(lform.password.data) == False):
            return redirect(url_for ('login'))
        login_user(student, remember=lform.remember_me.data)
        flash('The user {} has succesfully logged in! {}'.format(current_user.username, current_user.is_authenticated))
        return redirect(url_for('index'))
    return render_template('login.html', form = lform)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))