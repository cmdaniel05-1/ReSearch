from flask_wtf import FlaskForm
import sqlalchemy as sqla
from wtforms import IntegerField, StringField, SubmitField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

from app import db, login
from app.main.models import Student, Faculty


class LoginForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')
    
class StudentRegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', [Length(min=0, max=200)])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Post')
    
    def validate_username(self, username):
        query = sqla.select(Student).where(Student.username == username.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('This username already exists! Please use a diferent username.')
        query = sqla.select(Faculty).where(Faculty.username == username.data)
        faculty = db.session.scalars(query).first()
        if faculty is not None:
            raise ValidationError('This username already exists! Please use a diferent username.')
        
    def validate_email(self, email):
        query = sqla.select(Student).where(Student.email == email.data)
        student = db.session.scalars(query).first()
        if student is not None:
            raise ValidationError('The email already exists! Please use a different email.')
        
class FacultyRegistrationForm(FlaskForm):
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num = StringField('Phone Number', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Re-enter Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        query = sqla.select(Faculty).where(Faculty.username == username.data)
        faculty = db.session.scalars(query).first()
        if faculty is not None:
            raise ValidationError('This username already exists! Please use a diferent username.')
        
    def validate_email(self, email):
        query = sqla.select(Faculty).where(Faculty.email == email.data)
        faculty = db.session.scalars(query).first()
        if faculty is not None:
            raise ValidationError('The email already exists! Please use a different email.')