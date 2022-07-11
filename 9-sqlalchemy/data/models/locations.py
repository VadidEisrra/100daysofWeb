import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from data.sqlalchemybase import SqlAlchemyBase


class Location(SqlAlchemyBase):
    __tablename__ = 'locations'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    street = sa.Column(sa.String)
    city = sa.Column(sa.String, index=True)
    campus = sa.Column(sa.String, index=True)

    books = orm.relation('Book', back_populates='location')
