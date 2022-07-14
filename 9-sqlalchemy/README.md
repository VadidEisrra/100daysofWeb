# Library database project

blah blah blah this is epic


#### High level DB model

**Users** interact with system that keeps track of library books

**Checkout** correlates to a book that is removed from the library and assigned to a user for a period of time, 

**Books** that have a title, author etc

**Location** where books can be found to checkout or return

#### Starter code

The project begins with some utility libraries and the main program

```
db/
└── db_folder.py
infrastructure/
├── numbers.py
└── switchlang.py
program.py
```
- `db_folder.py` contains a function to return the full path of the db folder to create the sqlite database
- `numbers.py` contains a function to assist in parsing numbers
- `switchlang.py` is a module that provides switch blocks for Python. This is used in the main function of `program.py` to link actions to user input

## The app
`program.py` is a terminal application that loads a sqlite datebase (or imports data if there is none) and allows the user to interact with the data. It looks like this:
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
The functionality to make the database queries is not stored in the main program. They are written in `services/data_service.py`. This helps the code to be modular - if the database changes the queries can be re-written without touching the main program. Here is the the function to retrieve available books from the data service library  
`data_service.py`
```python
def available_books() -> List[Book]:
    session = session_factory.create_session()

    books = session.query(Book).filter(Book.location_id != None).all()
    return list(books)
```
This function creates a session to the database and queries books without a location, which is set to `Null` when they are checked out. There is no commit action to the session since no data is modified.

The session factory is yet another utility in `data/session_factory.py` that initializes connection to the database and handles the creation of tables as well as sessions used for any of the database actions in `data_service.py`

## Ok, but how are you modeling data

SQLAlchemy models for the database are stored in `data/models` directory
```
data
├── __all_models.py
├── models
│   ├── books.py
│   ├── checkout.py
│   ├── locations.py
│   └── users.py
├── session_factory.py
└── sqlalchemybase.py
```
Our model classes derive from a common base class `SqlAlchemyBase`. This base class is part of SQLAlchemy Declarative system that describes database tables and defines classes that are mapped to them. 

Within the Book class we define the table to be mapped to, and names and datatypes of columns in it. The Table object is created according to the specifications, and is associated with the class using the functionality derived from the `SqlAlchemyBase`.

Modeling a book in the database:
```python
import datetime

import sqlalchemy as sa
from sqlalchemy import orm

from data.sqlalchemybase import SqlAlchemyBase


class Book(SqlAlchemyBase):
    __tablename__ = 'books'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    created_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    title = sa.Column(sa.String, index=True)
    author = sa.Column(sa.String, index=True)

    location_id = sa.Column(sa.Integer,
                            sa.ForeignKey('locations.id'),
                            nullable=True)

    location = orm.relation('Location')
```
## How 'bout muh data

The initial action in main function of program.py is call a method to setup our database

```python
def main():
    setup_db()
...

def setup_db():
    global user
    session_factory.global_init('library.sqlite')
    session_factory.create_tables()
    import_data.import_if_empty()
    user = data_service.get_default_user()
```

Let's take a look at `data/session_factory.py`
```python
def global_init(db_name: str):
    global __engine, __factory

    if __factory:
        return

    conn_str = 'sqlite:///' + db_folder.get_full_path(db_name)
    __engine = sqlalchemy.create_engine(conn_str, echo=False)
    __factory = sqlalchemy.orm.sessionmaker(bind=__engine)


def create_tables():
    if not __engine:
        raise Exception("You have not called global_init()")

    import data.__all_models
    from data.sqlalchemybase import SqlAlchemyBase
    SqlAlchemyBase.metadata.create_all(__engine)


def create_session() -> sqlalchemy.orm.Session:
    if not __factory:
        raise Exception("You have not called global_init()")

    session: Session = __factory()
    session.expire_on_commit = False
    return session
```
#### global_init() aka engines and factories

The engine is the starting point for a SQLAlchemy application. It is very fancy; it interprets the underlying DBAPI python module functions as well as several flavor of database behavior.

A typical setup will associate the sessionmaker with an Engine, so that each Session generated will use this Engine to acquire connection resources. This association can be set up using the bind argument.

#### create_tables() from the model classes


- import all models defined in `data/__all_models.py`
- create tables for all classes derived from SqlAlchemyBase using the engine

###### create_all() will issue queries that first check for the existence of each individual table, and if not found will issue the CREATE statements

#### create_session() just db things

#### importing data for an empty database