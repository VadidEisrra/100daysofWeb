import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from data.models.checkout import Checkout
from data.sqlalchemybase import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, nullable=True, unique=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now, index=True)

    checkout = orm.relation("Checkout", order_by=[
        Checkout.start_time.desc(),
    ], back_populates='user')
