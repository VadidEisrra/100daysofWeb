from pyramid.view import view_config
from pyramid.request import Request

from bookdb.data import repository


@view_config(route_name='home', renderer='../templates/home/default.pt')
def home(_: Request):
    purchased_books = repository.get_purchased_books()
    non_purchased_books = repository.get_non_purchased_books()

    return {'project': 'Book Database',
            'purchased_books': purchased_books,
            'non_purchased_books': non_purchased_books
    }
