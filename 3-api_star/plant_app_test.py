from apistar import test

from plant_app import app, plants, PLANT_NOT_FOUND

client = test.TestClient(app)


def test_list_plants():
    response = client.get("/")
    assert response.status_code == 200
    plants = response.json()
    assert len(plants) == 1000
    assert type(plants) == list
    plant = plants[0]
    expected ={"id":1,"common_name":"Bristly Buttercup",
               "family":"Ranunculaceae",
               "scientific_name":"Ranunculus hispidus Michx. var. nitidus (Chapm.) T. Duncan"}
    assert plant == expected
    last_id = plants[-1]["id"]
    assert last_id == 1000


def test_create_plant():
    data = dict(common_name="a_plant",
                family="best_plant_family",
                scientific_name="Beautilis plantilus")
    response = client.post("/", data=data)
    assert response.status_code == 201
    assert len(plants) == 1001

    response = client.get("/1001/")
    assert response.status_code == 200
    expected ={"id":1001,"common_name":"a_plant",
               "family":"best_plant_family",
               "scientific_name":"Beautilis plantilus"}
    assert response.json() == expected


def test_create_plant_missing_fields():
    data = dict(key=1)
    response = client.post("/", data=data)
    assert response.status_code == 400

    errors = response.json()
    assert errors["common_name"] == "The \"common_name\" field is required."
    assert errors["family"] == "The \"family\" field is required."
    assert errors["scientific_name"] == "The \"scientific_name\" field is required."


def test_create_plant_field_validation():
    data = dict(common_name="x" * 100,
                family="x" * 100,
                scientific_name="x"* 200)
    response = client.post("/", data=data)

    errors = response.json()
    assert "Must have no more than 50 characters" in errors["common_name"]
    assert "Must have no more than 50 characters" in errors["family"]
    assert "Must have no more than 150 characters" in errors["scientific_name"]


def test_get_plant():
    response = client.get("/777/")
    assert response.status_code == 200
    expected ={"id":777,"common_name":"Muehlenberg's Astomum Moss",
               "family":"Pottiaceae",
               "scientific_name":"Astomum muehlenbergianum (Sw.) Grout"}
    assert response.json() == expected


def test_get_plant_not_found():
    response = client.get("/11111/")
    assert response.status_code == 404
    assert response.json() == {"error": PLANT_NOT_FOUND}


def test_update_plant():
    data = dict(common_name="your", family="mom", scientific_name="smells")
    response = client.put("/777/", data=data)
    assert response.status_code == 200

    expected={"id":777,"common_name":"your","family":"mom","scientific_name":"smells"}
    assert response.json() == expected

    response = client.get("/777/")
    assert response.json() == expected


def test_update_plant_notfound():
    data = dict(common_name="your", family="mom", scientific_name="smells")
    response = client.put("/11111/", data=data)
    assert response.status_code == 404
    assert response.json() == {"error": PLANT_NOT_FOUND}


def test_update_plant_validation():
    data = dict(common_name="x" * 100,
                family="x" * 100,
                scientific_name="x"* 200)
    response = client.put ("/777/", data=data)
    errors = response.json()
    assert "Must have no more than 50 characters" in errors["common_name"]
    assert "Must have no more than 50 characters" in errors["family"]
    assert "Must have no more than 150 characters" in errors["scientific_name"]


def test_delete_plant():
    plant_count = len(plants)

    for i in (11, 22, 33):
        response = client.delete(f"/{i}/")
        assert response.status_code == 204

        response = client.get(f"/{i}/")
        assert response.status_code == 404

    assert len(plants) == plant_count - 3
