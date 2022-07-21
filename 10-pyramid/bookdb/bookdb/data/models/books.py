import datetime
import sqlalchemy as sa
from bookdb.data.modelbase import SqlAlchemyBase

class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    title = sa.Column(sa.String, index=True)
    author = sa.Column(sa.String,  index=True)
    purchased = sa.Column(sa.String, index=True)
