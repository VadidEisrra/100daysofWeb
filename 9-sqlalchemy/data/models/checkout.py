import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from data.sqlalchemybase import SqlAlchemyBase


class Checkout(SqlAlchemyBase):
    __tablename__ = 'checkout'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)

    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    start_time = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)
    end_time = sa.Column(sa.DateTime, index=True)

    user_id = sa.Column(sa.Integer,
                                sa.ForeignKey('users.id'), nullable=False)
    user = orm.relation('User', back_populates='checkout')

    book_id = sa.Column(sa.String, sa.ForeignKey('books.id'), nullable=False)
    book = orm.relation('Book')

