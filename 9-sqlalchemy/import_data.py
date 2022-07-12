import datetime
import random

from data import session_factory
from data.models.locations import Location
from data.models.checkout import Checkout
from data.models.books import Book
from data.models.users import User
from services import data_service


def import_if_empty():
    __import_locations()
    __import_books()
    __import_users()
    __import_checkout()


def __import_books():
    session = session_factory.create_session()
    if session.query(Book).count() > 0:
        return

    titles = [
        'Three Thousand Lenses',
        'Isles of Meynard',
        'How To: Everything',
        'The Fall of Thoroh',
        'Elephant and Me',
        'Summit',
        'Feet Down, Head Up',
        'Early Settler Wood Working',
        'C Programming Language',
        'Cave Diving in Mexico',
    ]

    authors = [
        'Henry Collins',
        'Elijah Soumit',
        'Radjin Cahr',
        'Michal Dunning',
        'Crisvh Vishal',
        'Fally Sields',
        'Ross Faihrn',
        'Luz Paz',
        'Adam Saars',
        'Leonard pogh',
    ]

    locations = list(session.query(Location).all())

    for title in titles:
        b = Book()
        b.title = title
        b.author = random.choice(authors)
        b.location = random.choice(locations)
        session.add(b)

    session.commit()


def __import_users():
    session = session_factory.create_session()
    if session.query(User).count() > 0:
        return

    data_service.get_default_user()

    user2 = User()
    user2.email = 'user2@talkpython.fm'
    user2.name = 'user 2'
    session.add(user2)
    session.commit()


def __import_locations():
    session = session_factory.create_session()
    if session.query(Location).count() > 0:
        return

    location = Location()
    location.street = '493 32nd St.'
    location.city = 'Portland'
    location.campus = 'East Campus'
    session.add(location)

    location = Location()
    location.street = '1003 Canoe Blvd.'
    location.city = 'Portland'
    location.campus = 'West Campus'
    session.add(location)

    location = Location()
    location.street = '81 West Filtmore St.'
    location.city = 'Portland'
    location.campus = 'South Campus'
    session.add(location)

    session.commit()

def __import_checkout():
    session = session_factory.create_session()
    if session.query(Checkout).count() > 0:
        return

    books = list(session.query(Book))
    locations = list(session.query(Location))
    user = data_service.get_default_user()
    user2 = session.query(User).filter(User.email == 'user2@talkpython.fm').one()

    for _ in range(1, 3):
        selected = random.choice(books)
        data_service.issue_book(
            book=selected,
            user=user,
            start_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(1,100))
        )
        books.remove(selected)
        data_service.return_book(selected.id, random.choice(locations).id)

    for _ in range(1, 3):
        selected = random.choice(books)
        data_service.issue_book(
            book=selected,
            user=user2,
            start_date=datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 100))
        )
        books.remove(selected)
