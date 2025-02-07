from datetime import date, timezone
from typing import Optional

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

position_fields = db.Table(
    'position_fields',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key = True),
    sqla.Column('field_id', sqla.Integer, sqla.ForeignKey('field.id'), primary_key = True)
)

position_languages = db.Table(
    'position_languages',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key = True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key = True)
)
position_students = db.Table(
    'position_students',
    db.metadata,
    sqla.Column('position_id', sqla.Integer, sqla.ForeignKey('position.id'), primary_key = True),
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key = True)
)

student_languages = db.Table(
    'student_languages',
    db.metadata,
    sqla.Column('student_id', sqla.Integer, sqla.ForeignKey('student.id'), primary_key = True),
    sqla.Column('language_id', sqla.Integer, sqla.ForeignKey('language.id'), primary_key = True)
)

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    description : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    start_date: sqlo.Mapped[Optional[date]] = sqlo.mapped_column(default=lambda: date.today())
    end_date: sqlo.Mapped[Optional[date]] = sqlo.mapped_column(default=lambda: date.today())
    req_time : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    student_count : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)

    # Relationships
    fields : sqlo.Mapped[list['Field']] = sqlo.relationship(
        secondary = position_fields,
        primaryjoin = (position_fields.c.position_id == id),
        back_populates = 'positions'
    )
    languages : sqlo.Mapped[list['Language']] = sqlo.relationship(
        secondary = position_languages,
        primaryjoin = (position_languages.c.position_id == id),
        back_populates = 'positions'
    )
    students : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary = position_students,
        primaryjoin = (position_students.c.position_id == id),
        back_populates = 'positions'
    )

class Field(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))

    # Relationships
    positions : sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(
        secondary = position_fields,
        primaryjoin = (position_fields.c.field_id == id),
        back_populates = 'fields'
    )

class Student(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo. Mapped[str] = sqlo.mapped_column (sqla.String(64), index = True, unique = True)
    password_hash : sqlo.Mapped[Optional[str]] = sqlo.mapped_column(sqla.String(256))
    firstname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    lastname : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String (100))
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), index = True, unique = True)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    positions : sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(
        secondary = position_students,
        primaryjoin = (position_students.c.student_id == id),
        back_populates = 'students'
    )
    languages : sqlo.Mapped[list['Language']] = sqlo.relationship(
        secondary = student_languages,
        primaryjoin = (student_languages.c.position_id == id),
        back_populates = 'students'
    )

class Language(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))

    # Relationships
    positions : sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(
        secondary = position_languages,
        primaryjoin = (position_languages.c.language_id == id),
        back_populates = 'languages'
    )
    
    students : sqlo.WriteOnlyMapped['Student'] = sqlo.relationship(
        secondary = student_languages,
        primaryjoin = (student_languages.c.position_id == id),
        back_populates = 'students'
    )
