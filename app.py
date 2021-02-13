import requests
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

@app.route('/')
def index():
    api = 'http://api.openweathermap.org/data/2.5/weather?q={}&appid=2d9b0c570950eb4352f90aef452af0ae'
    city = 'Patna'

    if " " in city:
        city.replace(" ", "%20")

    url = api.format(city)
    weather_data = requests.get(url).json()
    print('bitch ... \n\n\n ~>')
    for _ in weather_data:
        print(_)

    return render_template('weather.html')


if __name__ == '__main__':
    app.run(debug=True)
