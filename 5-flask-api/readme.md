# Calling APIs in Flask

This project uses flask to present information from the NASA APOD and The Solar System OpenDATA APIs
## Overview

### Screenshot

![](https://github.com/VadidEisrra/100daysofWeb/blob/main/images/5-flask-api-index.png)
![](https://github.com/VadidEisrra/100daysofWeb/blob/main/images/5-flask-api-explore.png)

## My process

### Built with

- Flask
- HTML markup
- CSS custom properties

### What I learned

#### Passing data to the template

In `routes.py` a function to get the NASA APOD as well as a variable retrieving the current date in UTC are defined. We can pass these to the `render_template()` method as variables. 

###### Note `timenow` is *within* the index function of the `route()` decorator so time can be refreshed when the index is visited

```python
from Flask import render_template

def get_apod():
    r = requests.get("https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY")
    data = r.json()
    return data

apod = get_apod()


@app.route('/')
@app.route('/index')
def index():
    timenow = datetime.utcnow().strftime("%A %B %d, %Y - %H:%M:%S UTC")
    return render_template('index.html', time=timenow, apod=apod)
```

#### Handling POST requests and form data

By default, only `GET` requests are answered by a route. The `methods` argument of the `route()` decorator can be used to handle `POST` requests (in addition to other HTTP methods).

```python
from Flask import request

@app.route('/solar', methods=['GET', 'POST'])
def solarSystem():
    bodies = []
    solar_bodytype = ""
    if request.method == 'POST' and 'bodytype' in request.form:
        solar_bodytype = request.form.get('bodytype')
        bodies = get_solar_data(solar_bodytype)
    return render_template('solar.html', bodies=bodies,
                            solar_bodytype=solar_bodytype.capitalize())
```
The flask request object contains data the client sends to the app. Let's inspect these values with the form in `solar.html`

If we submit an empty form
```
(Pdb) request.form
ImmutableMultiDict([('bodytype', '')])
(Pdb) solar_bodytype
''
```
`asteroid` is submit into the form
```
(Pdb) request.form
ImmutableMultiDict([('bodytype', 'asteroid')])
(Pdb) solar_bodytype
'asteroid'
```
In `solar.html` the form input `name` attribute is used to reference the data
```html
    <form method ="POST" action"/solar">
      <label for=bodytype">Solar Body Type</label>
      <input type="text" id="bodytype" name="bodytype">
     <br>
    </form>
```

### Useful resources

- [Flask documentation](https://flask.palletsprojects.com/en/2.1.x/)
