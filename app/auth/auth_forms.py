from flask_wtf import FlaskForm
import sqlalchemy as sqla
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

from app import db, login
from app.main.models import Student, Faculty, User


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num = StringField('Phone Number', validators=[DataRequired()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_wpi_id(self, wpi_id):
        existing_user = User.query.filter_by(wpi_id=wpi_id.data).first()
        if existing_user:
            raise ValidationError('WPI ID is already in use. Please choose another.')
        
    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user:
            raise ValidationError('Username is already taken. Please choose another.')

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user:
            raise ValidationError('Email is already registered.')

class StudentRegistrationForm(RegistrationForm):
    pass
        
class FacultyRegistrationForm(RegistrationForm):
    pass
