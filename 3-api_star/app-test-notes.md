## Writing tests

API Star includes a test client that acts as an adapter for `requests` library, this allows you to make requests directly to your application

```python
from apistar import test
from myproject import app

client = test.TestClient(app)

def test_hello_world():
    response = client.get('/hello_world/')
    assert response.status_code == 200
    assert response.json() == ('hello': 'world'}
```

It's also not bound to any testing framework, so we'll use [pytest](https://www.pytest.org)

`app_test.py` skeleton

```python
from apistar import test

from app import app, cars

client = test.TestClient(app)

def test_list_cars():
    pass

def test_create_car():
    pass

def test_create_car_missing_fields():
    pass

def test_create_car_field_validation():
    pass

def test_get_car():
    pass

def test_get_car_notfound():
    pass

def test_update_car():
    pass

def test_update_car_notfound():
    pass

def test_update_car_validation():
    pass

def test_delete_car():
    pass
```

As an  example let's work on the `test_get_car()` function

First, define an endpoint response using the get method, we'll inspect this using a `breakpoint()`
```python
def test_get_car():
    response = client.get("/777/")
    breakpoint()
```
With the breakpoint set, run pytest and let's check out the status code and json in the response. From these values we can write assertions for test
```
(venv) user@computer 3-api_star % pytest app_test.py
======================================== test session starts =========================================
platform darwin -- Python 3.8.2, pytest-7.1.1, pluggy-1.0.0
rootdir: /Users/pf-dsierra/repos/100daysofWeb/3-api_star
collected 10 items                                                                                   

app_test.py ....
>>>>>>>>>>>>>>>>>>>>>>>>>>>>>> PDB set_trace (IO-capturing turned off) >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
--Return--
> /Users/user/repos/100daysofWeb/3-api_star/app_test.py(82)test_get_car()->None
-> breakpoint()
(Pdb) response.status_code
200
(Pdb) response.json()
{'id': 777, 'manufacturer': 'Ford', 'model': 'E-Series', 'year': 2004, 'vin': '1D7RV1CT8BS373093'}
(Pdb) expected = {'id': 777, 'manufacturer': 'Ford', 'model': 'E-Series', 'year': 2004, 'vin': '1D7RV1CT8BS373093'}
(Pdb) response.status_code == 200
True
(Pdb) response.json() == expected
True
(Pdb
```
Let's confirm our response status code is `200` and that the vehicle at index `777` is the one we want
```python
def test_get_car():
    response = client.get("/777/")
    assert response.status_code == 200 
    expected ={"id": 777, "manufacturer": "Ford",
               "model": "E-Series", "year": 2004,
               "vin": "1D7RV1CT8BS373093"}
    assert response.json() == expected
```
Check our test and voila!
```
(venv) user@computer 3-api_star % pytest app_test.py -v
======================================== test session starts =========================================
platform darwin -- Python 3.8.2, pytest-7.1.1, pluggy-1.0.0 -- /Users/pf-dsierra/repos/100daysofWeb/3-api_star/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/user/repos/100daysofWeb/3-api_star
collected 1 item                                                                                     

app_test.py::test_get_car PASSED                                                               [100%]

========================================= 1 passed in 0.26s ==========================================
```
Using this methodology, we can work out tests for basic CRUD functionality of the API
