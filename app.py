from flask import Flask, render_template, request, redirect, url_for
import requests
from datetime import date

API_KEY = "c5da7f6762e05a36fc3391a80e90e947"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

app = Flask(__name__)

def convert_to_nice_looking_date(date):
    # YYYY - MM - DD
    months = [
        "index_0", "January", "February", "March", "April", "May", "June", 
        "July", "August", "September", "October", "November", "December"
    ]
    pieces_of_date = str(date).split("-")
    year = pieces_of_date[0]
    day = int(pieces_of_date[2])
    month = months[int(pieces_of_date[1])]
    return f"{month} {day}, {year}"
    

def get_weather_data(cityinput): 
    city = cityinput.replace("_", " ").title()
    
    params = {
    "q": city,
    "appid": API_KEY,
    "units": "metric"
    }

    response = requests.get(BASE_URL, params=params)

    city_date = convert_to_nice_looking_date(date.today())

    if response.status_code == 200:
        data = response.json()
        city_temp = data['main']['temp']
        city_weather_description = data['weather'][0]['description']
        city_humidity = data['main']['humidity']
        city_wind_speed = data['wind']['speed']
        city_data = [
            city,
            city_temp,
            city_weather_description,
            city_humidity,
            city_wind_speed,
            city_date,
        ]
        return list(city_data)
        
        
    else:
        pass

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/<city_name>")
def city_home(city_name):
    city_data = get_weather_data(city_name)
    try:
        return render_template('weather.html', 
                           name = city_data[0], 
                           temp = city_data[1], 
                           weather_description = city_data[2],
                           humidity = city_data[3],
                           wind_speed = city_data[4],
                           today = city_data[5]
                           )
    except TypeError:
        return render_template('error.html')
        
@app.route("/input", methods= ['GET', 'POST'])
def submit_search():
    if request.method == 'POST':
        new_route = request.form.get('city_target')
        return redirect(url_for('/city_home', city_name=new_route))
    return render_template('index.html')
        
        
"""
Clear: Clear skies.
Sunny: Direct sunlight.
Partly cloudy: Some clouds in the sky.
Mostly cloudy: Mostly cloudy with some clear patches.
Overcast: Completely covered by clouds.
Light rain: Gentle rainfall.
Rain: Moderate rainfall.
Heavy rain: Intense rainfall.
Light snow: Light snowfall.
Snow: Moderate snowfall.
Thunderstorm: Storm with thunder and lightning.
Scattered clouds: Clouds scattered across the sky.
Broken clouds: A mix of clouds and clear skies, with some clouds covering the sky.
Few clouds: A small amount of clouds in the sky.
Scattered showers: Showers occurring in scattered locations.
Freezing drizzle: Drizzle that freezes upon contact with surfaces.
Sleet snow: A mix of rain and snow.
"""