import requests
import os
from flask import Flask, render_template
#from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.getenv("KEY")

app = Flask(__name__)

@app.route('/')
def index():
    api = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid={}'
    city = 'Las Vegas'

    url = api.format(city, API_KEY)
    weather_data = requests.get(url).json()

    data = {
            'city' : city,
            'temperature' : weather_data['main']['temp'],
            'description' :weather_data['weather'][0]['description'],
            'icon' : weather_data['weather'][0]['icon'],
            }


    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True)
