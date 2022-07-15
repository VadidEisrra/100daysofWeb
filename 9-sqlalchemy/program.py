import datetime
import sys
import import_data
from data import session_factory
from typing import List
from infrastructure.numbers import try_int
from infrastructure.switchlang import switch
from services import data_service

user = None


def main():
    setup_db()

    options = 'Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: '
    cmd = "NOT SET"

    while cmd:
        cmd = input(options).lower().strip()
        with switch(cmd) as s:
            s.case('c', checkout_book)
            s.case('a', find_available_books)
            s.case('l', locate_our_books)
            s.case('h', my_history)
            s.case('x', exit_app)
            s.default(lambda: print(f"Don't know what to do with {cmd}."))


def setup_db():
    global user
    session_factory.global_init('library.sqlite')
    session_factory.create_tables()
    import_data.import_if_empty()
    user = data_service.get_default_user()


def checkout_book():
    print("********** Checkout a book ********** ")
    books = find_available_books(True)
    chose_it = try_int(input('Which one do you want? ')) - 1

    if not (0 <= chose_it or chose_it < len(scooters)):
        print("Error: Pick another number.")
        return

    book = books[chose_it]
    data_service.issue_book(book, user, datetime.datetime.now())


def find_available_books(suppress_header=False):
    if not suppress_header:
        print("********** Available books: ********** ")

    available_books = data_service.available_books()
    for idx, b in enumerate(available_books, start=1):
        print(f"#{idx}. Title: {b.title}, "
              f"Author: {b.author}, Loc: {b.location.campus} {b.location.street}")

    print()
    return available_books


def locate_our_books():
    print("********** Current status of books ********** ")
    loaned_books = data_service.issued_books()
    available_books = data_service.available_books()

    print(f"Out with patrons [{len(loaned_books)} books]:")
    for b in loaned_books:
        print(f" {b.id} Title: {b.title}, Author: {b.author}, Account: {user.name}")

    print()

    print(f"Available [{len(available_books)} books]:")
    for b in available_books:
        print(f"Title: {b.title}, Author: {b.author}, "
              f"Loc: {b.location.campus} {b.location.street}")

    print()

def my_history():
    print("********** Your library history ********** ")
    user_local = data_service.get_default_user()
    for b in user_local.checkout:
        print(f" * {b.start_time.date().isoformat()} {b.book.title}")

    print()


def exit_app():
    print("")
    print("Bye!")
    sys.exit(0)


if __name__ == '__main__':
    main()
