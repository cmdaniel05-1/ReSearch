from datetime import date, timezone
from typing import Optional

from app import db
import sqlalchemy as sqla
import sqlalchemy.orm as sqlo

from werkzeug.security import generate_password_hash, check_password_hash

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

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    description : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    start_date : sqlo.Mapped[Optional[date]] = sqlo.mapped_column(sqla.Date)
    end_date : sqlo.Mapped[Optional[date]] = sqlo.mapped_column(sqla.Date)
    req_time : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)
    student_count : sqlo.Mapped[int] = sqlo.mapped_column(sqla.Integer)

    # Relationships
    fields : sqlo.WriteOnlyMapped['Field'] = sqlo.relationship(
        secondary = position_fields,
        primaryjoin = (position_fields.c.position_id == id),
        back_populates = 'positions'
    )
    languages : sqlo.WriteOnlyMapped['Language'] = sqlo.relationship(
        secondary = position_languages,
        primaryjoin = (position_languages.c.position_id == id),
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

class Language(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))

    # Relationships
    positions : sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(
        secondary = position_languages,
        primaryjoin = (position_languages.c.language_id == id),
        back_populates = 'languages'
    )

class Faculty(db.Model):
    faculty_id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    username : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(64), unique = True)
    email : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(120), unique = True)
    password_hash : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(256))
    name : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    phoneNum : sqlo.Mapped[int] = sqlo.mapped_column()

    positions : sqlo.WriteOnlyMapped['Position'] = sqlo.relationship(
        secondary = position_faculty,
        primaryjoin = (position_faculty.c.faculty_id == id),
        back_populates = 'faculty'
    )
    languages : sqlo.Mapped[list['Language']] = sqlo.relationship(
        secondary = faculty_languages,
        primaryjoin = (faculty_languages.c.faculty_id == id),
        back_populates = 'faculty'
    )

    def __repr__(self):
        return '<WPIID: {} - Username: {} - Name: {}>'.format(self.faculty_id, self.username, self.name)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)