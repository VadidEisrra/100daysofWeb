from pyramid.view import view_config
from pyramid.request import Request

from bookdb.data import repository


@view_config(route_name='home', renderer='../templates/home/default.pt')
def home(_: Request):
    books = repository.get_books()

    return {'project': 'Book Database',
            'books': books
    }
