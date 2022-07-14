# Library database project

This project is a bit more complex than other things I have worked on. This follows an introduction to SQLAlchemy. Much of the code was written for the example - I modified it for the library angle and tried to understand as much as I could without getting lost.


## High level DB model

**Users** interact with system that keeps track of library books

**Checkout** correlates to user getting book for period of time then returning it, retrieved and returned at particular location

**Books** that have a title, author etc

**Location** where books can be found to checkout or return

## Starter code

The project begins with some utility libraries

```
db/
└── db_folder.py
infrastructure/
├── numbers.py
└── switchlang.py
program.py
```

program.py is a terminal application that loads a sqlite datebase (or imports data if there is none) and allows the user to interact with the stored data. It looks like this:
``` 
Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: 
```
The primary function contains actions for each choice. For instance, if the user enters `a` the following function is executed  
`program.py`
```python
def find_available_books(suppress_header=False):
    if not suppress_header:
        print("********** Available books: ********** ")

    available_books = data_service.available_books()
    for idx, b in enumerate(available_books, start=1):
        print(f"#{idx}. Title: {b.title}, "
              f"Author: {b.author} Loc: {b.location.campus} {b.location.street}")

    print()
    return available_books
```
The functionality to make the database queries is not stored in the main program. They are written in `services/data_service.py`. This makes the main program modular - if the database changes the queries can be re-written without touching the main program. Here is the the function to retrieve available books from the data service library  
`data_service.py`
```python
def available_books() -> List[Book]:
    session = session_factory.create_session()

    books = session.query(Book).filter(Book.location_id != None).all()
    return list(books)
```
This function creates a session to the database and queries books without a location, which is set to `Null` when they are checked out. There is no commit action to the session since we are not modifying data.

The session factory is yet another utility that initializes connection to the database and handles the creation of tables as well as the sessions used for any of the queries in `data_service.py`