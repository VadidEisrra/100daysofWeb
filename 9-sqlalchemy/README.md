# Library database project

This is an introduction to SQLAlchemy, there is a lot of pre-written code for this exercise - hopefully I can make sense of the general flow here.


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
`program.py` is a terminal application that loads a sqlite datebase (or creates it if it doesn't exist) and allows the user to interact with the data. It looks like this:
``` 
Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: a
********** Available books: ********** 
#1. Title: Three Thousand Lenses, Author: Ross Faihrn, Loc: South Campus 81 West Filtmore St.
#2. Title: How To: Everything, Author: Adam Saars, Loc: South Campus 81 West Filtmore St.
#3. Title: The Fall of Thoroh, Author: Radjin Cahr, Loc: East Campus 493 32nd St.
#4. Title: Elephant and Me, Author: Ross Faihrn, Loc: East Campus 493 32nd St.
#5. Title: Summit, Author: Crisvh Vishal, Loc: West Campus 1003 Canoe Blvd.
#6. Title: Feet Down, Head Up, Author: Ross Faihrn, Loc: South Campus 81 West Filtmore St.
#7. Title: C Programming Language, Author: Adam Saars, Loc: East Campus 493 32nd St.
#8. Title: Cave Diving in Mexico, Author: Henry Collins, Loc: South Campus 81 West Filtmore St.

Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: 
```
The primary function contains actions for each choice. For instance, if the user enters `a` the following function is executed.  

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
The functionality to make the database queries is not stored in the main program. They are written in `services/data_service.py`. This helps the code to be modular - if the database changes the queries can be re-written without touching the main program. Here is the the function to retrieve available books from the data service library.  

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

`models/books.py`
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
## How 'bout muh database

### Setting up the DB
The initial action in main function of program.py is call a method to setup our database  

`program.py`
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
### Initializing and connecting to that DB
Let's take a look at the methods available in `data/session_factory.py`  

`data/session_factory.py`
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

The engine is the starting point for a SQLAlchemy application. It is very fancy; it interprets the underlying DBAPI python module as well as several flavor of database behavior.

A typical setup will associate the sessionmaker with an Engine, so that each session generated will use this engine to acquire connection resources. This association can be set up using the bind argument.

#### create_tables() from the model classes

In order to create tables, all models defined in `data/__all_models.py` are imported in addition to our SqlAlchemyBase class. The `create_all()` method creates tables for all imported classes that are derived from the base class.

###### create_all() will issue queries that first check for the existence of each individual table, and if not found will issue the CREATE statements

#### create_session() or getting a *handle* on things

We need a handle in order to interact with the database. A session instance, or more precisely an object of type `sqlalchemy.orm.session.Session` provides this. 

We create session objects each time we call the `sessionmaker()`, which in this case is defined as `__factory` - the session factory method bound to the engine object created in `global_init()`.

The session object is born!
```python
session : Session = __factory()
```

### Importing data to an EmptyDB TM

Say we've done some things but there is no data in our tables! Not to worry. Recall our `setup_db()` function in program.py. After initializing the database and creating tables we run a method imported from `import_data.py`. The specific method we call from this file is `import_if_empty()`  

`program.py`
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

Here is that method from `import_data.py`  

`import_data.py`
```python
def import_if_empty():
    __import_locations()
    __import_books()
    __import_users()
    __import_checkout()
```
Taking a look at first function `__import_locations()` we can see it queries the database and if there are zero locations in the table we generate some values and add them to the database. It's similar for the other tables.  

`import_data.py`
```python
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
```
## Where to from here

There is obviously more going on here than I've covered in this short introduction. Create a virtual environment, activate it, install requirements and run `program.py`!
```
Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: c
********** Checkout a book ********** 
#1. Title: Three Thousand Lenses, Author: Leonard pogh, Loc: East Campus 493 32nd St.
#2. Title: Isles of Meynard, Author: Michal Dunning, Loc: West Campus 1003 Canoe Blvd.
#3. Title: How To: Everything, Author: Henry Collins, Loc: West Campus 1003 Canoe Blvd.
#4. Title: The Fall of Thoroh, Author: Michal Dunning, Loc: South Campus 81 West Filtmore St.
#5. Title: Summit, Author: Radjin Cahr, Loc: East Campus 493 32nd St.
#6. Title: Early Settler Wood Working, Author: Radjin Cahr, Loc: East Campus 493 32nd St.
#7. Title: C Programming Language, Author: Michal Dunning, Loc: East Campus 493 32nd St.
#8. Title: Cave Diving in Mexico, Author: Ross Faihrn, Loc: East Campus 493 32nd St.

Which one do you want? 8
Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: h
********** Your library history ********** 
 * 2022-07-15 Cave Diving in Mexico
 * 2022-06-07 Three Thousand Lenses
 * 2022-04-24 Isles of Meynard

Enter a command, [c]heckout, [a]vailable, [l]ocate, [h]istory, e[X]it: 

```
