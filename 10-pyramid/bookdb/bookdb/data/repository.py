from typing import Optional
from typing import List

from bookdb.data.db_session import DbSession
from bookdb.data.models.books import Book


def get_books() -> List[Book]:
    session = DbSession.create_session()
    try:
        return session.query(Book).all()
    finally:
        session.close()


def get_book_by_id(book_id: int) -> Optional[Book]:
    session = DbSession.create_session()
    try:
        return session.query(Book) \
        .filter(Book.id == book_id) \
        .first()
    finally:
        session.close()
