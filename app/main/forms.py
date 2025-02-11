from flask_wtf import FlaskForm
from wtforms import FloatField, StringField, TextAreaField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
from app.main.models import Field, Language, Student, Faculty, User
import sqlalchemy as sqla
from flask_login import current_user

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description of project goals and objectives', [Length(min = 1, max = 1500)])
    start_date = DateField('Start date', validators=[DataRequired()])
    end_date = DateField('End date', validators=[DataRequired()])
    req_time = IntegerField('Hours per week', validators=[DataRequired()])
    student_count = IntegerField('Number of students wanted', validators=[DataRequired()])
    fields = QuerySelectMultipleField('Field',
                                      query_factory = lambda : db.session.scalars(sqla.select(Field)),
                                      get_label = lambda theField : theField.name,
                                      widget = ListWidget(prefix_label=False),
                                      option_widget=CheckboxInput())
    languages = QuerySelectMultipleField('Language',
                                         query_factory = lambda : db.session.scalars(sqla.select(Language)),
                                         get_label = lambda theLanguage : theLanguage.name,
                                         widget = ListWidget(prefix_label=False),
                                         option_widget=CheckboxInput())
    submit = SubmitField('Submit')

class FieldForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LanguageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password')
    password2 = PasswordField('Re-enter Password', validators=[EqualTo('password')])
    submit = SubmitField('Submit')
    
    def validate_wpi_id(self, wpi_id):
        existing_user = User.query.filter_by(wpi_id=wpi_id.data).first()
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError('WPI ID is already in use. Please choose another.')
        
    def validate_username(self, username):
        existing_user = User.query.filter_by(username=username.data).first()
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError('Username is already taken. Please choose another.')

    def validate_email(self, email):
        existing_user = User.query.filter_by(email=email.data).first()
        if existing_user and existing_user.id != current_user.id:
            raise ValidationError('Email is already registered.')
        
class StudentEditForm(EditForm):
    major = StringField("Major")
    gpa = FloatField("GPA")
    grad_date = DateField("Graduation Date")
    fields = QuerySelectMultipleField('Field',
                                      query_factory = lambda : db.session.scalars(sqla.select(Field)),
                                      get_label = lambda theField : theField.name,
                                      widget = ListWidget(prefix_label=False),
                                      option_widget=CheckboxInput())
    languages = QuerySelectMultipleField('Language',
                                         query_factory = lambda : db.session.scalars(sqla.select(Language)),
                                         get_label = lambda theLanguage : theLanguage.name,
                                         widget = ListWidget(prefix_label=False),
                                         option_widget=CheckboxInput())
        
class FacultyEditForm(EditForm):
    phone_num = StringField('Phone Number', validators=[DataRequired()])
