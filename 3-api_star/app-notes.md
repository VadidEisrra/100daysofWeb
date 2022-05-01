## Notes for plant app

Generate JSON data set from https://www.mockaroo.com or https://www.kaggle.com/

Create virtual environment  and install requirements

```
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
```

`app.py` skeleton
```python
import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_cars_data():
    pass

class Car(types.Type):
    pass

def list_cars(car: Car) -> JSONResponse:
    pass

def create_car(car: Car) -> JSONResponse:
    pass

def get_car(car_id: int) -> JSONResponse
    pass

def delete_car(car_id: int) -> JSONResponse:
    pass

routes = []

app = App(routes=routes)

if __name__ == '__main__':
Thanks 
routes = []

app = App(routes=routes)

if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
```

### `_load_cars_data()` function
The goal of this function is to read `cars.json` and return dictionary containing each vehicle. As we see below using just `json.loads()` returns each vehicle as a dictionary, what would be more helpful for interaction with the api is for vehicle to be identified individually. The functions at the end of the notes do just this; one using list comprehension and the other using traditional for loop style.

Create a variable type string ‘cars’ from contents of cars.json - contents are string
```python
With open(‘cars.json’) as f:
	cars = f.read()
```
Create a  variable type list ‘cars’ from contents of cars.json - contents of list are dictionaries. This is cool... but we don't really have an easy way to identify each vehicle
```python
With open(‘cars.json’) as f:
	cars = json.loads(f.read())

  {'id': 1000,
  'manufacturer': 'Bentley',
  'model': 'Mulsanne',
  'year': 2011,
  'vin': 'WBAPK5C50BA171421'}
```

The following functions perform the same action for the purpose of establishing an identifier key value for each vehicle definition: iterate over cars and return a new dictionary object containing each car (dict) with key value represented by the car id

`car_dict = {car["id"]: car for car in cars}`
```python
def test(car_dict):
    new_car_dict = {}
    for i in car_dict:
        new_car_dict.update({i["id"]: i})
    return new_car_dict

 1000: {'id': 1000,
  'manufacturer': 'Bentley',
  'model': 'Mulsanne',
  'year': 2011,
  'vin': 'WBAPK5C50BA171421'}
```
final function
```python
def _load_cars_data():
    with open('cars.json') as f:
        cars = json.loads(f.read())
        return {car["id"]: car for car in cars}
```

### `VALID_MANUFACTURERS` variable

`VALID_MANUFACTURERS` variable - this will be used to demo apistar validation

How can we easily generate a data structure containing only unique instances of vehicle
manufacturer strings?

Cars is a dictionary
~~~python
In [35]: type(cars)
Out[35]: dict
~~~
Each vehicle is a tuple of id: dict
<br>
Manufacturer is a key value pair within the vehicle dictionary
~~~python
In [56]: cars
Out[56]: 
{1: {'id': 1,
  'manufacturer': 'Toyota',
  'model': 'Previa',
  'year': 1993,
  'vin': '2C3CDXJG7FH063501'},
 2: {'id': 2,
  'manufacturer': 'Suzuki',
  'model': 'Sidekick',
  'year': 1990,
  'vin': '1FT7W2A64EE234371'},
 3: {'id': 3,
  'manufacturer': 'Chrysler',
  'model': 'Town & Country',
  'year': 2007,
  'vin': '5GAKRBKD7DJ950173'},
 4: {'id': 4,
  'manufacturer': 'Cadillac',
  'model': 'Fleetwood',
  'year': 1954,
  'vin': 'WBALW7C5XED593312'},
 5: {'id': 5,
  'manufacturer': 'Toyota',
  'model': '4Runner',
  'year': 1997,
  'vin': '1GYS4JKJ6FR049596'}}
~~~
So how do we access?
<br>
Using the `values()` method to return the values of a dictionary
~~~python
In [67]: for i in cars.values():
    ...:     print(i)
    ...: 
{'id': 1, 'manufacturer': 'Toyota', 'model': 'Previa', 'year': 1993, 'vin': '2C3CDXJG7FH063501'}
{'id': 2, 'manufacturer': 'Suzuki', 'model': 'Sidekick', 'year': 1990, 'vin': '1FT7W2A64EE234371'}
{'id': 3, 'manufacturer': 'Chrysler', 'model': 'Town & Country', 'year': 2007, 'vin': '5GAKRBKD7DJ950173'}
{'id': 4, 'manufacturer': 'Cadillac', 'model': 'Fleetwood', 'year': 1954, 'vin': 'WBALW7C5XED593312'}
{'id': 5, 'manufacturer': 'Toyota', 'model': '4Runner', 'year': 1997, 'vin': '1GYS4JKJ6FR049596'}
~~~
Well here comes set. Set is a method that returns only the unique values from a list. In this case we will pass a generator expression to the method
- List will place all items in memory
- Generator is iterator object that when called, yields one item at a time on demand
~~~python
In [22]: type([car["manufacturer"] for car in cars.values()])
Out[22]: list

In [19]: type(car["manufacturer"] for car in cars.values())
Out[19]: generator
~~~
Notice how list comprehension looks like generator expression passed to list constructor
~~~python
# list comprehension
cars = [car[“manufacturer”] for car in cars.values()]

# same as the list comprehension above
cars = list(car[“manufacturer”] for car in cars.values())
~~~
final variable
~~~python
VALID_MANUFACTURERS = set(car["manufacturer"] for car in cars.values())
~~~

### apistar `Type` class and method routes

We can use apistar type system to provide validation of incoming request data and serialization of outgoing response data

https://docs.apistar.com/type-system/

Create a Type class, describing a car as below

~~~python
class Car(types.Type):
    id = validators.Integer(allow_null=True)
    manufacturer = validators.String(enum=list(VALID_MANUFACTURERS))
    model = validators.String(max_length=50)
    year = validators.Integer(minimum=1900, maximum=2050)
    vin = validators.String(max_length=50, default='')

~~~

- validate `id` is an integer. Allow none when creating new cars (assigned in post)
- validate `manufacturer` by enumerating a list of valid strings
- validate `model` string of max length 50
- validate `year` integer of range 1900-2050
- validate `vin` string data, which is optional with default set to empty

Instantiate an app, establish routes

~~~python

routes = [ 
    route(‘/‘), method=‘GET’, handler=list_cars,
    route(‘/‘), method=‘POST’, handler=create_car,
    route(‘/{car_id/‘), method=‘GET’, handler=get_car,
    route(‘/{car_id/'), method=‘PUT’, handler=update_car,
    route(‘/{car_id/'), method=‘DELETE’, handler=delete_car,
]

app = App(routes=routes)

If __name__ == ‘__main__’:
    app.serve(‘127.0.0.1’, 5000, debug=True)
~~~

- routes establish the endpoint, method and handler

### creating `list_cars` api method
1. we use typing to hint list of objects of type Car is returned  
2. we want to return the cars in a list sorted by their ID  

Begin by loading only 5 cars and creating a list comprehension
```python
def _load_cars_data():
    with open('cars.json') as f:
        cars = json.loads(f.read())[:5]
        return {car["id"]: car for car in cars}
```

```python
from typing import List

def list_cars() -> List[Car]:
    return [car for car in cars]
```
But this only returns the vehicle id or index
<br>
Let's inspect the behavior by setting a `breakpoint()` after the function and running `app.py`
```python
(Pdb) test = [car for car in cars]
(Pdb) pp test
[1, 2, 3, 4, 5]
```
If we use `values()` method we can return the vehicle data
```python
(Pdb) test = [car for car in cars.values()]
(Pdb) pp test
[{'id': 1,
  'manufacturer': 'Toyota',
  'model': 'Previa',
  'vin': '2C3CDXJG7FH063501',
  'year': 1993},
 {'id': 2,
  'manufacturer': 'Suzuki',
  'model': 'Sidekick',
  'vin': '1FT7W2A64EE234371',
  'year': 1990},
 {'id': 3,
  'manufacturer': 'Chrysler',
  'model': 'Town & Country',
  'vin': '5GAKRBKD7DJ950173',
  'year': 2007},
 {'id': 4,
  'manufacturer': 'Cadillac',
  'model': 'Fleetwood',
  'vin': 'WBALW7C5XED593312',
  'year': 1954},
 {'id': 5,
  'manufacturer': 'Toyota',
  'model': '4Runner',
  'vin': '1GYS4JKJ6FR049596',
  'year': 1997}]
```
But we cannot sort on `cars.values()`
```python
(Pdb) pp sorted(cars.values())
*** TypeError: '<' not supported between instances of 'dict' and 'dict'
```
We can however sort on `items()` since it returns a list of the tuple items
```python
(Pdb) pp sorted(cars.items())
[(1,
  {'id': 1,
   'manufacturer': 'Toyota',
   'model': 'Previa',
   'vin': '2C3CDXJG7FH063501',
   'year': 1993}),
 (2,
  {'id': 2,
   'manufacturer': 'Suzuki',
   'model': 'Sidekick',
   'vin': '1FT7W2A64EE234371',
   'year': 1990}),
 (3,
  {'id': 3,
   'manufacturer': 'Chrysler',
   'model': 'Town & Country',
   'vin': '5GAKRBKD7DJ950173',
   'year': 2007}),
 (4,
  {'id': 4,
   'manufacturer': 'Cadillac',
   'model': 'Fleetwood',
   'vin': 'WBALW7C5XED593312',
   'year': 1954}),
 (5,
  {'id': 5,
   'manufacturer': 'Toyota',
   'model': '4Runner',
   'vin': '1GYS4JKJ6FR049596',
   'year': 1997})]
```
Great! But the items are returned as tuple, so let's select the tuple element with data
```python
(Pdb) test = [car[1] for car in sorted(cars.items())]
(Pdb) pp test
[{'id': 1,
  'manufacturer': 'Toyota',
  'model': 'Previa',
  'vin': '2C3CDXJG7FH063501',
  'year': 1993},
 {'id': 2,
  'manufacturer': 'Suzuki',
  'model': 'Sidekick',
  'vin': '1FT7W2A64EE234371',
  'year': 1990},
 {'id': 3,
  'manufacturer': 'Chrysler',
  'model': 'Town & Country',
  'vin': '5GAKRBKD7DJ950173',
  'year': 2007},
 {'id': 4,
  'manufacturer': 'Cadillac',
  'model': 'Fleetwood',
  'vin': 'WBALW7C5XED593312',
  'year': 1954},
 {'id': 5,
  'manufacturer': 'Toyota',
  'model': '4Runner',
  'vin': '1GYS4JKJ6FR049596',
  'year': 1997}]
```
Lastly, let's wrap that element in an instance of Car for validation/serialization
```python
(Pdb) test = [Car(car[1]) for car in sorted(cars.items())]
(Pdb) pp test
[<Car(id=1, manufacturer='Toyota', model='Previa', year=1993, vin='2C3CDXJG7FH063501')>,
 <Car(id=2, manufacturer='Suzuki', model='Sidekick', year=1990, vin='1FT7W2A64EE234371')>,
 <Car(id=3, manufacturer='Chrysler', model='Town & Country', year=2007, vin='5GAKRBKD7DJ950173')>,
 <Car(id=4, manufacturer='Cadillac', model='Fleetwood', year=1954, vin='WBALW7C5XED593312')>,
 <Car(id=5, manufacturer='Toyota', model='4Runner', year=1997, vin='1GYS4JKJ6FR049596')>]
```
### `get_car` GET method

```python
def get_car(car_id: int) -> JSONResponse:
    car = cars.get(car_id)
    if not car:
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, 404)

    return JSONResponse(Car(car), 200)
```
`get_car` takes an integer arg `car_id` and returns JSONResponse object of Car type
- get() method on cars dictionary to search for car_id
- if None is returned, error is a dictionary used in the JSONResponse
- else return JSONReponse of serialized Car object and status code 200 

### `create_car` POST method
```python
def create_car(car: Car) -> JSONResponse:
    car_id = len(cars) + 1 
    car.id = car_id
    cars[car_id] = car 
    return JSONResponse(Car(car), 201)
```
`create_car` takes dict input and returns data in JSONResponse object of Car type
- calculate `car_id` by taking len of car dict + 1 
- since car input data (dict) sent by user does not contain an id, set object id using calculated car_id (don't really understand how this works)
- update cars dict in memory (normally this would be db operation)
- return serialized data of car using Car class

### `update_car` PUT method
```python
def update_car(car_id: int, car: Car) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    car.id = car_id
    cars[car_id] = car 
    return JSONResponse(Car(car), status_code=200)
```
`update_car` takes car id and modifies existing car attributes
- get() method to search for car id, return error if none
- set object id to provided int 
- update cars dict in memory with new car 
- return serialized car object

### `delete_car` DELETE method
```python
def delete_car(car_id: int) -> JSONResponse:
    if not cars.get(car_id):
        error = {'error': CAR_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del cars[car_id]
    return JSONResponse({}, status_code=204)
```
`delete_car` takes car id and removes it from the dictionary
- get() method to search for car id, return error if none
- delete car from cars dictionary
- return JSONResponse containing empty dict and 204
