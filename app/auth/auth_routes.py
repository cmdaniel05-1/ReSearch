from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db
from app.auth import auth_blueprint as auth
from app.auth.auth_forms import RegistrationForm, LoginForm
from app.main.models import Student, Faculty, User
import sqlalchemy as sqla


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    rform = RegistrationForm()
    if rform.validate_on_submit():
        if rform.type.data == "Faculty":
            user = Faculty(wpi_id = rform.wpi_id.data,
                                username = rform.username.data,
                                firstname = rform.firstname.data,
                                lastname = rform.lastname.data,
                                email = rform.email.data,
                                phone_num = rform.phone_num.data)
        else:
            user = Faculty(wpi_id = rform.wpi_id.data,
                                username = rform.username.data,
                                firstname = rform.firstname.data,
                                lastname = rform.lastname.data,
                                email = rform.email.data,
                                phone_num = rform.phone_num.data)
        user.set_password(rform.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('main.index'))
    return render_template('register.html', form = rform)

@auth.route('/login', methods = ['GET', 'POST'])
def login():
    lform = LoginForm()
    if lform.validate_on_submit():
        query = sqla.select(User).where(User.username == lform.username.data)
        user = db.session.scalars(query).first()

        if user is None or not user.check_password(lform.password.data):
            flash("Invalid username or password")
            return redirect(url_for('auth.login'))

        login_user(user, remember=lform.remember_me.data)
        flash('The user {} has successfully logged in!'.format(current_user.username))
        return redirect(url_for('main.index'))
    return render_template('login.html', form = lform)

@auth.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))