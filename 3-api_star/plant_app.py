import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse


def _load_plants_data():
    with open('plants.json') as f:
        plants = json.loads(f.read())
        return {plant["id"]: plant for plant in plants}


plants = _load_plants_data()
VALID_NAMES = set([plant["common_name"]
                   for plant in plants.values()])
PLANT_NOT_FOUND = 'Plant not found'


class Plant(types.Type):
    id = validators.Integer(allow_null=True)
    common_name = validators.String(max_length=50)
    family = validators.String(max_length=50)
    scientific_name = validators.String(max_length=150)


def list_plants() -> List[Plant]:
    return [Plant(plant[1]) for plant in sorted(plants.items())]


def create_plant(plant: Plant) -> JSONResponse:
    plant_id = len(plants) + 1
    plant.id = plant_id
    plants[plant_id] = plant
    return JSONResponse(Plant(plant), status_code=201)


def get_plant(plant_id: int) -> JSONResponse:
    plant = plants.get(plant_id)
    if not plant:
        error = {'error': PLANT_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    return JSONResponse(Plant(plant), status_code=200)


def update_plant(plant_id: int, plant: Plant) -> JSONResponse:
    if not plants.get(plant_id):
        error = {'error': PLANT_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    plant.id = plant_id
    plants[plant_id] = plant
    return JSONResponse(Plant(plant), status_code=200)


def delete_plant(plant_id: int) -> JSONResponse:
    if not plants.get(plant_id):
        error = {'error': PLANT_NOT_FOUND}
        return JSONResponse(error, status_code=404)

    del plants[plant_id]
    return JSONResponse({}, status_code=204)


routes = [
    Route('/', method='GET', handler=list_plants),
    Route('/', method='POST', handler=create_plant),
    Route('/{plant_id}/', method='GET', handler=get_plant),
    Route('/{plant_id}/', method='PUT', handler=update_plant),
    Route('/{plant_id}/', method='DELETE', handler=delete_plant),
]

app = App(routes=routes)


if __name__ == '__main__':
    app.serve('127.0.0.1', 5000, debug=True)
