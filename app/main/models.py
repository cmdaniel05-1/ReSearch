from datetime import date, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db, login
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id)) or None


position_fields = db.Table(
    'position_fields',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key = True),
    sqla.Column('field_id', sqla.Integer, sqla.ForeignKey('field.id'), primary_key = True)
)
student_fields = db.Table(
    'student_fields',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key = True),
    sqla.Column('field_id', sqla.Integer, sqla.ForeignKey('field.id'), primary_key = True)
)

position_languages = db.Table(
    'position_languages',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key = True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key = True)
)

student_languages = db.Table(
    'student_languages',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key = True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key = True)
)
    
class User(db.Model, UserMixin):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    wpi_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer(), unique= True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), index = True, unique = True)
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String (100))
    password_hash : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), index = True, unique = True)
    phone_num: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(20))
    type: sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(50)) #'user' or 'faculty'

    def __repr__(self):
        return '<Id: {} - WPI ID: {} - Username: {} - First Name: {} - Last Name: {}>'.format(self.id,
                                                                                              self.wpi_id,
                                                                                              self.username,
                                                                                              self.firstname,
                                                                                              self.lastname)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    __mapper_args__ = {
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }


class Student(User):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)

    #additional information
    major : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), nullable = True)
    gpa: sqlo.Mapped[float] = sqlo.mapped_column(sqla.Float, nullable = True)
    grad_date: sqlo.Mapped[date] = sqlo.mapped_column(sqla.Date, nullable = True)


    # Relationships
    applications : sqlo.Mapped[list['Application']] = sqlo.relationship(back_populates='student_applied')
    languages : sqlo.Mapped[list['Language']] = sqlo.relationship(
        secondary = student_languages,
        back_populates = 'students'
    )
    fields : sqlo.Mapped[list['Field']] = sqlo.relationship(
        secondary = student_fields,
        back_populates = 'students'
    )

    __mapper_args__ = {
        'polymorphic_identity': 'student'
    }

    def is_applied(self, position):
        result = db.session.query(Application).filter(
            Application.student_id == self.id,
            Application.position_id == position.id
        ).first()
        return result is not None
    
    #returns true if student is available
    def is_available(self):
        for application in self.applications:
            if application.app_is_accepted:
                return False
        return True



    def apply(self, new_position, reference, statement):
        if not self.is_applied(new_position):
            new_application = Application(position_id = new_position.id,
                                          student_id = self.id,
                                          reference_id = reference.id,
                                          statement = statement)
            db.session.add(new_application)
            db.session.commit()

    def withdraw(self, position):
        if self.is_applied(position):
            application = db.session.query(Application).filter(
                Application.position_id == position.id,
                Application.student_id == self.id
            ).first()
        
            if application:  # Ensure application exists before deletion
                db.session.delete(application)
                db.session.commit()

    def get_applications(self):
        # Query the Application table and filter by student_id
        return db.session.query(Application).filter(Application.student_id == self.id).all()


class Faculty(User):
    id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer, sqla.ForeignKey('user.id'), primary_key=True)

    # Relationships
    positions : sqlo.Mapped['Position'] = sqlo.relationship(back_populates='faculty')
    reference_requests : sqlo.Mapped['Application'] = sqlo.relationship(back_populates='reference')

    __mapper_args__ = {
        'polymorphic_identity': 'faculty',
    }

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    faculty_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Faculty.id), index=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    description : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    start_date: sqlo.Mapped[Optional[date]] = sqlo.mapped_column(default=date.today)
    end_date: sqlo.Mapped[Optional[date]] = sqlo.mapped_column(default=date.today)
    req_time : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    student_count : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)

    # Relationships
    applicants : sqlo.Mapped[list['Application']] = sqlo.relationship(back_populates='applied_position')
    faculty : sqlo.Mapped[Faculty] = sqlo.relationship(back_populates='positions')
    fields : sqlo.Mapped[list['Field']] = sqlo.relationship(
        secondary = position_fields,
        back_populates = 'positions'
    )
    languages : sqlo.Mapped[list['Language']] = sqlo.relationship(
        secondary = position_languages,
        back_populates = 'positions'
    )

class Application(db.Model):
    student_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Student.id), primary_key=True)
    position_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Position.id), primary_key=True)
    app_is_accepted : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=None, nullable=True)
    statement : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(500))

    reference_id : sqlo.Mapped[int] = sqlo.mapped_column(sqla.ForeignKey(Faculty.id), primary_key=True)
    ref_is_accepted : sqlo.Mapped[bool] = sqlo.mapped_column(sqla.Boolean, default=None, nullable=True)

    # Relationships
    student_applied : sqlo.Mapped[Student] = sqlo.relationship(back_populates='applications')
    applied_position : sqlo.Mapped[Position] = sqlo.relationship(back_populates='applicants')
    reference : sqlo.Mapped[Faculty] = sqlo.relationship(back_populates='reference_requests')

class Field(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)

    # Relationships
    positions : sqlo.Mapped['Position'] = sqlo.relationship(
        secondary = position_fields,
        back_populates = 'fields'
    )
    students : sqlo.Mapped[list['Student']] = sqlo.relationship(
        secondary = student_fields,
        back_populates = 'fields'
    )

class Language(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100), unique=True)

    # Relationships
    positions : sqlo.Mapped['Position'] = sqlo.relationship(
        secondary = position_languages,
        back_populates = 'languages'
    )
    students : sqlo.Mapped[list['Student']] = sqlo.relationship(
        secondary = student_languages,
        back_populates = 'languages'
    )