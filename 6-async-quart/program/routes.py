import aiohttp
import asyncio
import requests
from program import app
from quart import request
from quart import render_template

from datetime import datetime


async def get_apod():
    url =  "https://api.nasa.gov/planetary/apod?api_key=DEMO_KEY"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            data = await resp.json()
    return data

apod = asyncio.run(get_apod())

@app.route('/')
@app.route('/index')
async def index():
    timenow = datetime.utcnow().strftime("%A %B %d, %Y - %H:%M:%S UTC")
    return await render_template('index.html', time=timenow, apod=apod)


#@app.route('/solar', methods=['GET', 'POST'])
#async def solarSystem():
#    bodies = []
#    solar_bodytype = ""
#    if request.method == 'POST' and 'bodytype' in request.form:
#        solar_bodytype = request.form.get('bodytype')
#        bodies = get_solar_data(solar_bodytype)
#    return render_template('solar.html', bodies=bodies,
#                            solar_bodytype=solar_bodytype.capitalize())
#
#
#async def get_solar_data(solar_bodytype):
#    url = f"https://api.le-systeme-solaire.net/rest/bodies/?filter=bodyType,eq,{solar_bodytype.lower()}"
#    async with aiohttp.ClientSession as session:
#        async with session.get(url) as resp:
#            resp.raise_for_status
#            data = await resp.json()
#    bodies = []
#    for l in data.values():
#        for d in l:
#            bodies.append(d.get("englishName"))
#    return bodies
