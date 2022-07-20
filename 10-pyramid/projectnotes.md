# Pyramid web framework

[Pyramid](https://trypyramid.com/) is we web framework for python, let's build something with it!

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