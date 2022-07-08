import datetime
import random
from typing import List

from data import session_factory
from data.models.rentals import Rental
from data.models.scooters import Scooter
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


def book_scooter(scooter: Scooter, user: User, start_date: datetime.datetime) -> Rental:
    rental = None

    return rental


def park_scooter(scooter_id: int, location_id: int) -> Scooter:
    scooter = None

    return scooter


def rented_scooters() -> List[Scooter]:
    scooters = []

    return list(scooters)


def parked_scooters() -> List[Scooter]:
    scooters = []

    return list(scooters)
