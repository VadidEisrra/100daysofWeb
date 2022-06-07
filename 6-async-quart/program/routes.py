import aiohttp
import asyncio
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


async def get_solar_data(solar_bodytype):
    url = f"https://api.le-systeme-solaire.net/rest/bodies/?filter=bodyType,eq,{solar_bodytype.lower()}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status
            data = await resp.json()
    bodies = []
    for l in data.values():
        for d in l:
            bodies.append(d.get("englishName"))
    return bodies


apod = asyncio.run(get_apod())


@app.route('/')
@app.route('/index')
async def index():
    timenow = datetime.utcnow().strftime("%A %B %d, %Y - %H:%M:%S UTC")
    return await render_template('index.html', time=timenow, apod=apod)


@app.route('/solar', methods=['GET', 'POST'])
async def solarSystem():
    bodies = []
    solar_bodytype = ""
    form = await request.form
    if request.method == 'POST' and 'bodytype' in form:
        solar_bodytype = form.get('bodytype')
        bodies = await get_solar_data(solar_bodytype)
    return await render_template('solar.html', bodies=bodies,
                                solar_bodytype=solar_bodytype.capitalize())
