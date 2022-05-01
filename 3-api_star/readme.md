## Building APIs with API Star (0.5.4.1)

**Important**: `apistar` version `0.5.41` let you build complete APIs. 

If you look at the [project docs](https://docs.apistar.com) today though, you'll see the following note:

> _Where did the server go?_ With version 0.6 onwards the API Star project is being focused as a framework-agnositic suite of API tooling. The plan is to build out this functionality in a way that makes it appropriate for use either as a stand-alone tool, or together with a large range of frameworks. The 0.5 branch remains available on GitHub, and can be installed from PyPI with `pip install apistar==0.5.41`.

For this reason and in order for the project to work it uses version `0.5.41`.

This project uses a data set from [Mockaroo](https://mockaroo.com/) and loads it into a `list` of `dict`s for data store simplification

`plant_app.py` serves basic CRUD functionality for the data found in `plants.json`

```
(venv) user@computer 3-api_star % python plant_app.py
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 116-959-169
127.0.0.1 - - [01/May/2022 08:40:36] "GET /10/ HTTP/1.1" 200 -
127.0.0.1 - - [01/May/2022 08:40:50] "DELETE /10/ HTTP/1.1" 204 -
127.0.0.1 - - [01/May/2022 08:40:54] "GET /10/ HTTP/1.1" 404 -
```
Examples using curl

```
user@computer 3-api_star % curl -v http://127.0.0.1:5000/10/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> GET /10/ HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.64.1
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Server: Werkzeug/2.1.2 Python/3.8.2
< Date: Sun, 01 May 2022 12:28:16 GMT
< content-length: 97
< content-type: application/json
< Connection: close
< 
* Closing connection 0
{"id":10,"common_name":"Corrigiola","family":"Caryophyllaceae","scientific_name":"Corrigiola L."}
```

```
user@computer 3-api_star % curl -v -X "DELETE" http://127.0.0.1:5000/10/
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> DELETE /10/ HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.64.1
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 204 No Content
< Server: Werkzeug/2.1.2 Python/3.8.2
< Date: Sun, 01 May 2022 12:32:18 GMT
< content-length: 2
< content-type: application/json
< Connection: close
< 
* Excess found in a non pipelined read: excess = 2 url = /10/ (zero-length body)
* Closing connection 0
```

```
user@computer 3-api_star % curl -v http://127.0.0.1:5000/10/            
*   Trying 127.0.0.1...
* TCP_NODELAY set
* Connected to 127.0.0.1 (127.0.0.1) port 5000 (#0)
> GET /10/ HTTP/1.1
> Host: 127.0.0.1:5000
> User-Agent: curl/7.64.1
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 404 Not Found
< Server: Werkzeug/2.1.2 Python/3.8.2
< Date: Sun, 01 May 2022 12:32:45 GMT
< content-length: 27
< content-type: application/json
< Connection: close
< 
* Closing connection 0
{"error":"Plant not found"}
```

## Testing with pytest
Included is a basic test suite using API Star built in test library
```python
(venv) user@computer 3-api_star % pytest -v
====================================================== test session starts ======================================================
platform darwin -- Python 3.8.2, pytest-7.1.2, pluggy-1.0.0 -- /Users/pf-dsierra/repos/100daysofWeb/3-api_star/venv/bin/python3
cachedir: .pytest_cache
rootdir: /Users/user/repos/100daysofWeb/3-api_star
collected 10 items                                                                                                              

plant_app_test.py::test_list_plants PASSED                                                                                [ 10%]
plant_app_test.py::test_create_plant PASSED                                                                               [ 20%]
plant_app_test.py::test_create_plant_missing_fields PASSED                                                                [ 30%]
plant_app_test.py::test_create_plant_field_validation PASSED                                                              [ 40%]
plant_app_test.py::test_get_plant PASSED                                                                                  [ 50%]
plant_app_test.py::test_get_plant_not_found PASSED                                                                        [ 60%]
plant_app_test.py::test_update_plant PASSED                                                                               [ 70%]
plant_app_test.py::test_update_plant_notfound PASSED                                                                      [ 80%]
plant_app_test.py::test_update_plant_validation PASSED                                                                    [ 90%]
plant_app_test.py::test_delete_plant PASSED                                                                               [100%]

====================================================== 10 passed in 0.35s =======================================================
```
