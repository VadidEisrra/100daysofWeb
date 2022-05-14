# Flask Intro

### 1. Install and Setup Flask

First we need to initialize the virtual environment for use with flask, once it is created activate it and install flask  

- `python3 -m venv venv`
- `source ./venv/bin/activate`
- `pip install flask`

### 2. Setup your Flask app as a package

Project hierarchy
~~~
.
├── demo.py
├── program
       ├── __init__.py
       ├── routes.py
~~~  

Program directory will house the package

`__init__.py` file denotes this is a python package  
`routes.py` file contains the routes or links for the flask app  

### 3. Create init.py
`__init__.py` will configure our package

~~~python
from flask import Flask

app = Flask(__name__)

from program import routes
~~~
- `from flask import Flask` imports the __Flask__ class
- `app = Flask(__name__)` creates an instance of the class, the first argument is the name of the application's module or package. `__name__` is a convenient shortcut appropriate for most cases. This is needed so Flask knows where to look for resources such as templates and static files
- `from program import routes` import routes file to be used with the instance

### 4. Define Flask app routes in routes.py
`routes.py`

 ~~~python
from program import app

@app.route('/')
@app.route('/index')

def index():
    return 'Hello world'
~~~
- `from program import app` imports the flask app object created in `__init__.py` file
- `@app.route` decorators tell Flask what URL should trigger the function `index()`, here `/` and `/index` provide basically the same URL
- The function `index` will run when the index URL is called. General note: *name functions similar to the URL that calls them*

### 5. Run your Flask app!

`demo.py`  
~~~python
from program import app
~~~
Essentially `demo.py` will be called by flask at runtime to point to the app we've defined in our package `program`

set environment variable `FLASK_APP=demo.py` before `flask run`

By importing `app` from our package, we are executing package `__init__.py` which:
- creates flask instance
- executes `routes.py` establishing URL routing for instance  

### 6. Persistent FLASK_APP environment var

To make variable persistent within venv install python-dotenv and create env file for flask  
`pip install python-dotenv`  
`vim .flaskenv`
```
FLASK_APP=demo.py
```

### 7. Create basic index.html template

Define a new index function in `routes.py` that uses the `render_template` method against `index.html`  

`routes.py`
~~~python
from program import app
from flask import render_template

@app.route('/')
@app.route('/index')

#def index():
#    return 'Hello world'

def index():
    return render_template('index.html')
~~~

Then we will create a `templates` folder with a new `index.html` template
~~~
.
├── demo.py
├── program
        ├── __init__.py
        ├── routes.py
        └── templates
            └── index.html
~~~
`index.html`
~~~html
<html>
    <head>
        <title>This is our site</title>
    </head>

    <body>
        <p>This is the text we've included in our HTML file</p>
    </body>
~~~
### 8. Creating base.html template

A base template will provide consistency across site pages. 
- Site title will remain the same for every page
- We use Jinja placeholders within the body since that content will differ by page

`base.html`
~~~html
<html>
    <head>
        <title>This is our site</title>
    </head>

    <body>
        {% block content %}{% endblock %}
    </body>
~~~

Now, to make this useful we modify `index.html` to provide the content we want to render using the `base.html` template

`index.html`
~~~jinja
{% extends "base.html" %}

{% block content %}
        <h1>Hello~</h1>
        <p>This is text we've included in our HTML file</p>
{% endblock %}
~~~

- The `extends` tag is tells the template engine that `index.html` inherits `base.html`
- When `index.html` is rendered, `base.html` is rendered with block content from `index.html ` 

### 9. New template for 100DaysofCode

- Create a new template called 100days.html that inherits base.html with some changes to the block content  
- Add url target to routes.py  

`100days.html`
~~~jinja
{% extends 'base.html' %}

{% block content %}
    <h1>Hello! Congrats on taking the challenge \o/</h1>
    <p>This is text from 100 days of html</p>
{% endblock %}
~~~

`routes.py`
~~~python
from program import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/100days')
def p100days():
    return render_template('100days.html')
~~~

### 10. Using css, create menu bar

New `base.html` includes some [mui css](https://www.muicss.com/)
~~~html
<html>
  <head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <!-- load MUI -->
    <link href="//cdn.muicss.com/mui-0.10.3/css/mui.min.css" rel="stylesheet" type="text/css" />
    <script src="//cdn.muicss.com/mui-0.10.3/js/mui.min.js"></script>
  </head>
  <body>
      <div class="mui-panel">Menu Bar -
        <button class="mui-btn mui-btn--raised"><a href="/index">Home</a></button>
        <button class="mui-btn mui-btn--raised"><a href="/100Days">100 Days</a></button>
      </div>
      <hr>
      {% block content %}{% endblock %}
  </body>
</html>
~~~
