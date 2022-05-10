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


@app.route('/chuck')
def chuck():
    joke = get_chuck_joke()
    return render_template('chuck.html', joke=joke)


@app.route('/pokemon', methods=['GET', 'POST'])
def pokemon():
    pokemon = []
    if request.method == 'POST' and 'pokecolour' in request.form:
        color = request.form.get('pokecolour')
        pokemon = get_pokemon_color(color)
    return render_template('pokemon.html', pokemon=pokemon)


def get_chuck_joke():
    r = requests.get('https://api.chucknorris.io/jokes/random')
    data = r.json()
    return data['value']


def get_pokemon_color(color):
    url = f"https://pokeapi.co/api/v2/pokemon-color/{color.lower()}"
    r = requests.get(url)
    pokedata = r.json()
    pokemon = [i['name'] for i in pokedata['pokemon_species']]
    return pokemon
