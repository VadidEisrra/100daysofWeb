from pyramid.httpexceptions import HTTPFound
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


@view_config(route_name='home',
             renderer='../templates/home/default.pt',
             request_method='POST')
def home_post(request: Request):

    book_id = int(request.POST.get('book_id'))
    repository.mark_book_purchased(book_id)

    raise HTTPFound(location='/')
