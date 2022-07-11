import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from data.sqlalchemybase import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    title = sa.Column(sa.String, index=True)
    author = sa.Column(sa.String, index=True)

    # todo: relationships
    location_id = sa.Column(sa.Integer,
                            sa.ForeignKey('locations.id'),
                            nullable=True)

    location = orm.relation('Location')
