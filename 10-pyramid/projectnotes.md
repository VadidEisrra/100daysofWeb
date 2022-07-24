# Pyramid

[Pyramid](https://trypyramid.com/) is web framework for python, let's build something with it!

## Project setup
1. Install [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/installation.html)  
`pip install cookiecutter`
2. Verify cookiecutter is in $PATH  
`where cookiecutter`
3. Run cookiecutter on [Pyramid cookiecutter starter template](https://github.com/Pylons/pyramid-cookiecutter-starter) and select project options  
`$ cookiecutter https://github.com/Pylons/pyramid-cookiecutter-starter`
```
project_name [Pyramid Scaffold]: Book Database
repo_name [book_database]: bookdb
Select template_language:
1 - jinja2
2 - chameleon
3 - mako
Choose from 1, 2, 3 [1]: 2
Select backend:
1 - none
2 - sqlalchemy
3 - zodb
Choose from 1, 2, 3 [1]: 1
```
4. Complete setup (be sure to activate virtual environment) and run
```
Change directory into your newly created project.
    cd bookdb

Create a Python virtual environment.
    python3 -m venv env

Upgrade packaging tools.
    env/bin/pip install --upgrade pip setuptools

Does this in tutorial (symlink + dependencies?)
	env/bin/pip python setup.py develop
    
Install the project in editable mode with its testing requirements.
    env/bin/pip install -e ".[testing]"

Run your project's tests.
    env/bin/pytest

Run your project.
    env/bin/pserve development.ini
```
## Project structure

Bit of organization from defaults. `mytemplate.py` is renamed to `default.py` plus a new stylesheet `site.css` is created for additional custom styling. Don't forget to update image and template references in the templates themselves as well as the views.
```
├── __init__.py
├── routes.py
├── static
│   ├── css
│   │   ├── site.css
│   │   └── theme.css
│   ├── img
│   │   ├── pyramid-16x16.png
│   │   └── pyramid.png
│   └── js
├── templates
│   ├── errors
│   │   └── 404.pt
│   ├── home
│   │   └── default.pt
│   └── shared
│       └── layout.pt
└── views
    ├── __init__.py
    ├── default.py
    └── notfound.py
```
## Database
#### Building the SQLAlchemy model
```
bookdb/bookdb
.
├── __init__.py
├── bin
│   └── load_base_data.py
├── data
│   ├── __all_models.py
│   ├── __init__.py
│   ├── db_session.py
│   ├── modelbase.py
│   ├── models
│   │   ├── __init__.py
│   │   └── books.py
│   └── repository.py
├── db
│   ├── MOCK_BOOKS.json
│   └── book_db.sqlite
```

- `db/MOCK_BOOKS.json` - generated data from [mockaroo](https://www.mockaroo.com/)  
- `/data/models/books.py` - SQLAlchemy model for the books
- `data/db_session.py` - methods to initialize and create sessions to the sqlite db
- `data/repository.py` - methods we will use to run specific queries against the db
- `bin/load_base_data.py` - methods can be called to build the db if it doesn't exist on startup

#### Putting it all together
The function to initialize the database is added to the main method of the pyramid project's `__init__.py`  
`bookdb/bookdb/__init__.py`
```python
import os

from bookdb.bin import load_base_data
from bookdb.data.db_session import DbSession

from pyramid.config import Configurator


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
        config.include('.routes')
        config.scan()

    init_db() # Hello!

    return config.make_wsgi_app()


def init_db():
    db_file = os.path.join(
        os.path.abspath(os.path.dirname(__file__)),
        'db',
        'book_db.sqlite'
    )   
    DbSession.global_init(db_file)
    load_base_data.load_starter_data()
```