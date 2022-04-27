from apistar import test

from app import app, cars

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
