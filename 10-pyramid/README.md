# Python web frameworks - Pyramid

[Pyramid](https://trypyramid.com/) is a really cool web framework for python! This is a small exercise that implements a sqlite backend using primarily pyramid and SQLAlchemy. The setup is detailed in `projectnotes.md`.

## Overview

The project is a super basic super small book database - a list of books that have and have yet to be purchased. The task is simple: present a visitor those books, and allow them to mark books when they have been purchased.

### Screenshot

![](https://github.com/VadidEisrra/100daysofWeb/blob/main/images/10-Pyramid.png)


## My process

### Built with

- Pyramid
- SQLAlchemy
- SQLite
- Chameleon templates
- HTML markup
- Bootstrap CSS
- Mockaroo

### What I learned

#### Integrating database operations with the frontend

In the previous project that explored the basics of SQLAlchemy I put together a terminal application to interact with data. Here, we extend that by simply migrating those database methods to the views in Pyramid. BTW views are just code you can execute in response to requests made to your application. 

For instance, when we visit the hoe page the function `def home()` is called, this function

- retrives books from our database
- passes the book data to be rendered in the home page template (`default.pt`)

```python
@view_config(route_name='home', renderer='../templates/home/default.pt')
def home(_: Request):
    purchased_books = repository.get_purchased_books()
    non_purchased_books = repository.get_non_purchased_books()

    return {'project': 'Book Database',
            'purchased_books': purchased_books,
            'non_purchased_books': non_purchased_books
    }
```
Awesome!

#### Boostrap... sort of

All of the styling (lol) is from bootstrap. I haven't used this in a formal setting I did finagle with some of the grid column layout that became relatively intuitive after reading through some of the [docs](https://getbootstrap.com/docs/5.2/getting-started/introduction/). While I do celebrate it's ease of use, I also am aware the importance to minimize external dependencies within your projects - keeping that in mind Bootstrap has come a long way and I for sure will be exploring it in the future.


### Useful resources

- [Pyramid](https://trypyramid.com/)
- [Boostrap](https://getbootstrap.com/docs/5.2/getting-started/introduction/)
- [SQLAlchemy](https://www.sqlalchemy.org/)


