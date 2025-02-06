from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, DateField, IntegerField
from wtforms.validators import DataRequired, Length
from wtforms_sqlalchemy.fields import QuerySelectMultipleField
from wtforms.widgets import ListWidget, CheckboxInput

from app import db
from app.main.models import Field, Language
import sqlalchemy as sqla

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

