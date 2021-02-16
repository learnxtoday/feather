"""
All the views for our weather application
Currently we support the following 3 views:

1. **Home** - The main view for weather (jump to section in [[app.py#home]] )
2. **Add** - called to add a new city (jump to section in [[app.py#add]] )
3. **Delete** - called to delete a city's weather data (jump to section in [[app.py#delete]] )

"""

import requests
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("KEY")


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'this-too-shall-pass'

db = SQLAlchemy(app)

# === Models for Weather app ===

class City(db.Model):
    """
    The City class defines the main storage point for weather.
    Each entry has two fields:
    id - stores the primary key ID of the city
    city - used to display the name of the city on screen
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)



def get_weather_data(city):
    api = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'
    url = api.format(city, API_KEY)
    r = requests.get(url).json()

    return r

# === home ===

@app.route('/')
def index_get():
    """
    The cities are queried from the databse and a GET request is sent to the
    openweathermap API with the city and API key as parameters.
    The need-to-know details are extracted from the JSON response and appended to a list.
    Which in turn in parsed to the template using Jinja2.
    """
    cities = City.query.all()
    weather_data = []

    for city in cities:
        r = get_weather_data(city.name)

        weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' :r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
                }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)

# === add ===

@app.route('/', methods=['POST'])
def index_post():
    error_msg = ""
    new_city = request.form.get('city')

    if new_city:
        existing_city = City.query.filter_by(name=new_city).first()

        if not existing_city:
            new_city_data = get_weather_data(new_city)
            if new_city_data['cod'] == 200:
                new_city_obj = City(name=new_city)
                db.session.add(new_city_obj)
                db.session.commit()
            else:
                error_msg = "City does not exist in the world!"
        else:
            error_msg = "City already exists in the database!"

    if error_msg:
        flash(error_msg, 'error')
    else:
        flash("City added successfully")

    return redirect(url_for('index_get'))

# === delete ===

@app.route('/delete/<name>')
def delete_city(name):
    city = City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()

    # since I am in the route, i can reefrence the object as it exists even if city data is deleted. but only while the link is active/in session
    flash(f'Successfully deleted { city.name }', 'success')
    return redirect(url_for('index_get'))

if __name__ == '__main__':
    app.run()
