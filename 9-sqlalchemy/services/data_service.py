import datetime
import random
from typing import List

from data import session_factory
from data.models.checkout import Checkout
from data.models.books import Book
from data.models.users import User


def get_default_user():
    session = session_factory.create_session()

    user = session.query(User).filter(User.email == 'test@talkpython.fm').first()
    if user:
        return user

    user = User()
    user.email = 'test@talkpython.fm'
    user.name = 'Test user 1'
    session.add(user)

    session.commit()

    return user


def issue_book(book: Book, user: User, start_date: datetime.datetime) -> Checkout:
    session = session_factory.create_session()

    book = session.query(Book).filter(Book.id == book.id).one()
    book.location_id = None

    checkout = Checkout()
    checkout.book_id = book.id
    checkout.user_id = user.id
    checkout.start_time = start_date
    checkout.end_time = checkout.start_time + datetime.timedelta(days=4)

    session.add(checkout)
    session.commit()


def return_book(book_id: int, location_id: int) -> Book:
    session = session_factory.create_session()

    book = session.query(Book).filter(Book.id == book_id).one()
    book.location_id = location_id

    session.commit()

    return book


def issued_books() -> List[Book]:
    session = session_factory.create_session()

    books = session.query(Book).filter(Book.location_id == None).all()

    return list(books)

def available_books() -> List[Book]:
    session = session_factory.create_session()

    books = session.query(Book).filter(Book.location_id != None).all()

    return list(books)
