from apistar import test

from app import app, cars, CAR_NOT_FOUND

client = test.TestClient(app)


def test_list_cars():
    response = client.get('/')
    assert response.status_code == 200
    cars = response.json()
    assert len(cars) == 1000
    assert type(cars) == list
    car = cars[0]
    expected = {'id': 1, 'manufacturer': 'Toyota',
                'model': 'Previa', 'year': 1993,
                'vin': '2C3CDXJG7FH063501'}
    assert car == expected
    last_id = cars[-1]['id']
    assert last_id == 1000


def test_create_car():
    data = dict(manufacturer='Toyota',
                   model='Previa',
                   year=2018,
                   vin='123')
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(cars) == 1001

    response = client.get('/1001/')
    assert response.status_code == 200
    expected = {'id': 1001, 'manufacturer': 'Toyota',
                'model': 'Previa', 'year': 2018,
                'vin': '123'}
    assert response.json() == expected


    data = dict(manufacturer='Lotus',
                   model='Evora',
                   year=2022,
                   vin='456')
    response = client.post('/', data=data)
    assert response.status_code == 201
    assert len(cars) == 1002

    response = client.get('/1002/')
    assert response.status_code == 200
    expected = {'id': 1002, 'manufacturer': 'Lotus',
                'model': 'Evora', 'year': 2022,
                'vin': '456'}
    assert response.json() == expected


def test_create_car_missing_fields():
    data = dict(key=1)
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors['manufacturer'] == 'The "manufacturer" field is required.'
    assert errors['model'] == 'The "model" field is required.'
    assert errors['year'] == 'The "year" field is required.'


def  test_create_car_field_validation():
    data = dict(manufacturer="Opel",
                model="x" * 51,
                year="2051")
    response = client.post('/', data=data)
    assert response.status_code == 400

    errors = response.json()
    assert "Must be one of" in errors["manufacturer"]
    assert "Must have no more than 50 characters." in errors["model"]
    assert "Must be less than or equal to 2050." in errors["year"]


def test_get_car():
    data = dict(manufacturer="Ford",
                model="E-Series",
                year="2004",
                vin="1D7RV1CT8BS373093")
    response = client.get('/777/')
    assert response.status_code == 200
    expected ={'id': 777, 'manufacturer': 'Ford',
			   'model': 'E-Series', 'year': 2004,
               'vin': '1D7RV1CT8BS373093'}
    assert response.json() == expected


def test_get_car_notfound():
    response = client.get('/11111/')
    assert response.status_code == 404
    assert response.json() == {'error': CAR_NOT_FOUND}
