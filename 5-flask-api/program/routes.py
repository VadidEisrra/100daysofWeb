import requests
from program import app
from flask import request
from flask import render_template

from datetime import datetime


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


@app.route('/solar', methods=['GET', 'POST'])
def solarSystem():
    bodies = []
    solar_bodytype = ""
    if request.method == 'POST' and 'bodytype' in request.form:
        solar_bodytype = request.form.get('bodytype')
        bodies = get_solar_data(solar_bodytype)
    return render_template('solar.html', bodies=bodies,
                            solar_bodytype=solar_bodytype.capitalize())


def get_solar_data(solar_bodytype):
    url = f"https://api.le-systeme-solaire.net/rest/bodies/?filter=bodyType,eq,{solar_bodytype.lower()}"
    r = requests.get(url)
    bodydata = r.json()
    bodies = []
    for l in bodydata.values():
        for d in l:
            bodies.append(d.get("englishName"))
    return bodies
