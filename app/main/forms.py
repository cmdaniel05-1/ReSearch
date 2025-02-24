
from flask.debughelpers import _dump_loader_info
from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, StringField, TextAreaField, SubmitField, DateField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, ValidationError, EqualTo, Email, Optional
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
from app.main.models import Field, Language, Student, Faculty, User
import sqlalchemy as sqla
from flask_login import current_user

def validate_checkbox(form, checkbox):
    if not checkbox.data:
        raise ValidationError("Please select at least one checkbox.")

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

class AddFieldForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        existing_field = Field.query.filter_by(name=name.data).first()
        if existing_field:
            raise ValidationError('Field already exists.')

class DeleteFieldForm(FlaskForm):
    fields = QuerySelectMultipleField ('Remove Fields',
                query_factory = lambda : db.session.scalars(sqla.select(Field).order_by(Field.name)),
                get_label = lambda theField : theField.name,
                widget=ListWidget(prefix_label=False),
                option_widget=CheckboxInput(),
                validators=[validate_checkbox])
    submit = SubmitField('Submit')

class AddLanguageForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_name(self, name):
        existing_language = Language.query.filter_by(name=name.data).first()
        if existing_language:
            raise ValidationError('Language already exists.')

class DeleteLanguageForm(FlaskForm):
    languages = QuerySelectMultipleField ('Remove Languages',
                query_factory = lambda : db.session.scalars(sqla.select(Language).order_by(Language.name)),
                get_label = lambda thelanguage : thelanguage.name,
                widget=ListWidget(prefix_label=False),
                option_widget=CheckboxInput(),
                validators=[validate_checkbox])
    submit = SubmitField('Submit')

class EditForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired()])
    firstname = StringField('First Name',validators=[DataRequired()])
    lastname = StringField('Last Name', validators=[DataRequired()])
    wpi_id = IntegerField('WPI ID', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone_num = StringField('Phone Number', validators=[DataRequired()])
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
    major = StringField("Major", validators=[Optional()])
    gpa = FloatField("GPA", validators=[Optional()])
    grad_date = DateField("Graduation Date", validators=[Optional()])
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
    pass

class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class ApplicationForm(FlaskForm):
    statement = TextAreaField('Why are you interested in this position and what do you hope to gain?', [Length(min = 1, max = 500)])
    reference = SelectField('Reference name and email:')
    submit = SubmitField('Submit')

        
class UpdateStatusForm(FlaskForm):
     app_status = SelectField('Select an option:', 
                          choices=[('Approve', 'Approve'), ('Pending', 'Pending'), ('Reject', 'Reject'), ('', 'Select an option')], 
                          validators=[DataRequired()],
                          default='')
     ref_status = SelectField('Select an option:', 
                          choices=[('Approve', 'Approve'), ('Pending', 'Pending'), ('Reject', 'Reject'), ('', 'Select an option')], 
                          validators=[DataRequired()],
                          default='')
     submit = SubmitField('Submit')

     def validate_status(self, field):
         if field.data == '':
            raise ValidationError("Please choose a valid option")
             
        