import json
import os
import random
from typing import List

import dateutil.parser
from sqlalchemy.orm import Session

from bookdb.data.db_session import DbSession
from bookdb.data.models.books import Book


def load_starter_data():
    print("Loading starter data...")
    session = DbSession.create_session()
    if session.query(Book).counter() > 0:
        session.close()
        print("Data already loaded...")
        return

    session.expire_on_commit = False

    add_books()

    session.commit()
    session.close()


def add_books():
    data_file = os.path.join(DbSession.db_folder, 'MOCK_BOOKS.json')
    with open(data_file, 'r', encoding='utf-8') as fin:
        data = json.load(fin)

    for b in data:

        book = Book()
        book.created_date = dateutil.parser.parse(b.get('created_date'))
        book.title = b.get('book_title')
        book.author = b.get('book_author')
        book.purchased = b.get('purchased')
