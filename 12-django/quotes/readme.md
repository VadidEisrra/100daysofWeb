# Django

Let's have some fun with one of the most popular Python web frameworks!

## Setup

Create the demo project folder, virtual environment and install django

```
cd quotes
python3 -m venv venv
source venv/bin/activate
pip install django
```
Create a django project in current directory
```
django-admin startproject mysite .
```
Create our application within the project
```
django-admin startapp quotes
```

### Configure Django

Set SECRET_KEY and DEBUG values in`mysite/settings.py` to point to our virtual environment settings so they are not hardcoded in Django (don't forget to `import os`)

`SECRET_KEY = os.environ['SECRET_KEY']`

`DEBUG = os.environ.get('DEBUG', False)`

Add the values to `venv/bin/activate` script so they are available in the virtualenv
```
export SECRET_KEY=$SECRET_KEY
export DEBUG=True
```
Add our app `quotes` to the list of installed quotes in `mysite/settings.py`
```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'quotes'
]
```
Create a central template directory and define a base template

```
quotes % mkdir mysite/templates
quotes % touch mysite/templates/base.html
```
Link to `mysite/settings.py` `TEMPLATES` dirs

`'DIRS': [os.path.join(BASE_DIR, 'mysite/templates')],`

## URL routing and first view

To creat our first URL route and view

- define a default route in the main app URLs to point to our quotes app URLs
- define a URL pattern in our quotes app that maps to a view
- create a views file for the quotes app, define a basic view that receives a request and returns a response

Add default URL to `mysite/urls.py` that redirects to `quotes.urls`

`mysite/urls.py`  
```python
from django.contrib import admin
from django.urls import include, path

urlpatterns = [ 
    path('', include('quotes.url')),
    path('my-backend/', admin.site.urls),
]
```
Let's create `quotes/urls.py` that will be referenced by the default URL in `mysite/urls.py`

`quotes/urls.py`  
```python
from django.urls import path

from . import views

urlpatterns = [ 
    path('', views.index, name='index'),
]
```
The URL pattern will now point to a basic view written in `quotes.views.py`

`quotes/views.py`  
```python
from django.http import HttpResponse

def index(request):
    return HttpResponse('Welceme to Django')
```
## Django models and db migrations

#### Defining the model

Django's ORM allows us to write Python classes that map to a database table. Here is the model for a quote. Each class attribute maps to a database field

```python
from django.db import models

class Quote(models.Model):
    quote = models.TextField()
    author = models.CharField(max_length=100)
    source = models.URLField(blank=True, null=True)
    cover = models.URLField(blank=True, null=True)
    added = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.quote} - {self.author}'

    class Meta:
        ordering = ['-added']
```

- `URLField` provides URL validation 
- `DateTimeFields` convert data to datetime objects
- To make a field optional is to use `null=True`
- `blank=True` makes it optional within a form
- `auto_now_add` sets date when instance is created  
- `auto_now` updates field when record is updated  

To have object display more meaningful information in admin layer or django shell define `__str__` method that returns the quote and author

meta class defines ordering that will be used to displays most recent quote

#### Performing migration

Before syncing to the database, Django needs to create migrations (SQL commands) from the models in models.py. To do that we use `makemigrations`

```
(venv) quotes % python manage.py makemigrations
Migrations for 'quotes':
  quotes/migrations/0001_initial.py
    - Create model Quote
```
Once the migrations are created we can execute the SQL commands from the migrations on the database using `migrate`

```
(venv) quotes % python manage.py migrate
Operations to perform:
  Apply all migrations: admin, auth, contenttypes, quotes, sessions
Running migrations:
  Applying quotes.0001_initial... OK
```
#### Inspect the SQLite database

```quotes % sqlite3 db.sqlite3
SQLite version 3.32.3 2020-06-18 14:16:19
Enter ".help" for usage hints.
sqlite> .tables
auth_group                  django_admin_log          
auth_group_permissions      django_content_type       
auth_permission             django_migrations         
auth_user                   django_session            
auth_user_groups            quotes_quote              
auth_user_user_permissions
sqlite> .schema quotes_quote
CREATE TABLE IF NOT EXISTS "quotes_quote" ("id" integer NOT NULL PRIMARY KEY AUTOINCREMENT, "quote" text NOT NULL, "author" varchar(100) NOT NULL, "source" varchar(200) NULL, "cover" varchar(200) NULL, "added" datetime NOT NULL, "edited" datetime NOT NULL);
```

#### Viewing ORM from Django shell

Let's open the django shell
```python
(venv) quotes % python manage.py shell
Python 3.8.2 (default, Dec 21 2020, 15:06:04) 
[Clang 12.0.0 (clang-1200.0.32.29)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
```
In the shell we can import our Quote class
```python
>>> from quotes.models import Quote
>>> Quote
<class 'quotes.models.Quote'>
```
Let's add a quote using the `Quote` class, include some attributes and save the quote to the database

We can view all quote objects, notice the `__str__` class method returning the quote and author
```python
>>> quote = Quote(quote='Get busy living or get busy dying.', author='Stephen King')
>>> quote
<Quote: Get busy living or get busy dying. - Stephen King>
>>> quote.save()
>>> Quote.objects.all()
<QuerySet [<Quote: Get busy living or get busy dying. - Stephen King>]>
```
Add a few more quotes
```
>>> quote = Quote(quote='Great minds discuss ideas; average minds discuss events; small minds discuss people.', author='Eleanor Roosevelt')
>>> quote.save()
>>> Quote.objects.count()
2
>>> quote = Quote(quote='Those who dare to fail miserably can achieve greatly.', author='John F. Kennedy')
>>> quote.save()
>>> Quote.objects.count()
3
>>> Quote.objects.all()
<QuerySet [<Quote: Those who dare to fail miserably can achieve greatly. - John F. Kennedy>, <Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Eleanor Roosevelt>, <Quote: Get busy living or get busy dying. - Stephen King>]>
```
Let's filter quotes for the author `Stephen King`, then search for quotes with the letter `k` in the author name
```python
>>> Quote.objects.filter(author='Stephen King')
<QuerySet [<Quote: Get busy living or get busy dying. - Stephen King>]>
>>> 
>>> Quote.objects.filter(author__icontains='k')
<QuerySet [<Quote: Those who dare to fail miserably can achieve greatly. - John F. Kennedy>, <Quote: Get busy living or get busy dying. - Stephen King>]>
>>> 
>>> Quote.objects.filter(author__icontains='r')
<QuerySet [<Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Eleanor Roosevelt>]>
```
Let's grab a quote whose author name contains the letter `k` and edit the author field

Notice the filter returns a `QuerySet`, to grab the actual quote we can use the list index

Once we have the quote we can modify it's attributes (in this case the author) and save it

Running the filter again we see the updated author
```python
>>> quote = Quote.objects.filter(author__icontains='r')
>>> quote
<QuerySet [<Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Eleanor Roosevelt>]>
>>> 
>>> type(quote)
<class 'django.db.models.query.QuerySet'>
>>> quote = Quote.objects.filter(author__icontains='r')[0]
>>> 
>>> quote
<Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Eleanor Roosevelt>
>>> 
>>> type(quote)
<class 'quotes.models.Quote'>
>>> 
>>> quote.author = 'Anna Eleanor Roosevelt'
>>> 
>>> quote.save()
>>> 
>>> quote = Quote.objects.filter(author__icontains='r')
>>> 
>>> Quote.objects.filter(author__icontains='r')
<QuerySet [<Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Anna Eleanor Roosevelt>]>
>>> 
>>> Quote.objects.filter(author__icontains='r')[0].author
'Anna Eleanor Roosevelt'
```
To remove a quote, assign a variable from the filter and delete it
```python
>>> quote = Quote.objects.filter(author__icontains='r')
>>> quote
<QuerySet [<Quote: Great minds discuss ideas; average minds discuss events; small minds discuss people. - Anna Eleanor Roosevelt>]>
>>> quote.delete()
(1, {'quotes.Quote': 1})
>>> Quote.objects.count()
2

```