from flask import render_template, flash, redirect, url_for
from flask_login import login_user, current_user, logout_user, login_required
from app import db, oauth
from app.auth import auth_blueprint as auth
from app.auth.auth_forms import RegistrationForm, LoginForm
from app.main.models import Student, Faculty, User
import sqlalchemy as sqla
import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for


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
            user = Student(wpi_id = rform.wpi_id.data,
                                username = rform.username.data,
                                firstname = rform.firstname.data,
                                lastname = rform.lastname.data,
                                email = rform.email.data,
                                phone_num = rform.phone_num.data)
        user.set_password(rform.password.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Congratulations, you are now a registered {}!'.format(rform.type.data))
        return redirect(url_for('main.index'))
    return render_template('register.html', form = rform)

@auth.route('/login/sso')
def sso_login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True)
    )

@auth.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    user = session.get("user")
    info = user["userinfo"]
    query = sqla.select(User).where(User.email == info["email"])
    user = db.session.scalars(query).first()

    if user is None:
        flash("Email not recognized, register an account befor using sso")
        return redirect(url_for('auth.sso_logout'))

    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/logout/sso')
@login_required
def sso_logout():
    session.clear()
    return redirect(
        "https://" + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("auth.login", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )

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
    if session:
        return redirect(url_for('auth.sso_logout'))
    return redirect(url_for('auth.login'))

@auth.route("/home")
def home():
    return render_template("home.html", session=session.get('user'), pretty=json.dumps(session.get('user'), indent=4))