import requests
import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("KEY")


app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'

db = SQLAlchemy(app)


class City(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        new_city = request.form.get('city')

        if new_city:
            new_city_obj = City(name=new_city)
            db.session.add(new_city_obj)
            db.session.commit()


    cities = City.query.all()

    api = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid={}'

    weather_data = []

    for city in cities:

        url = api.format(city.name, API_KEY)
        r = requests.get(url).json()

        weather = {
                'city' : city.name,
                'temperature' : r['main']['temp'],
                'description' :r['weather'][0]['description'],
                'icon' : r['weather'][0]['icon'],
                }

        weather_data.append(weather)

    return render_template('weather.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run()
