from datetime import date, timezone
from typing import Optional

from app import db
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

class Position(db.Model):
    id : sqlo.Mapped[int] = sqlo.mapped_column(primary_key=True)
    title : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(100))
    description : sqlo.Mapped[str] = sqlo.mapped_column(sqla.String(1500))
    start_date : sqlo.Mapped[Optional[date]] = sqlo.mapped_column(date.now(timezone.utc))
    end_date : sqlo.Mapped[Optional[date]] = sqlo.mapped_column(date.now(timezone.utc))
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
        primaryjoin = (position_languages.c.language == id),
        back_populates = 'languages'
    )