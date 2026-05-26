from flask import Flask, render_template, jsonify, request
import requests
import os

app = Flask(__name__)

API_KEY = "951f7b83a8c15be6dfa68c62b8b5af06"  
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "imperial"  # change to "metric" for Celsius
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        return None
    data = response.json()

    temp = data["main"]["temp"]
    feels_like = data["main"]["feels_like"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    description = data["weather"][0]["description"]
    cloud_cover = data["clouds"]["all"]
    icon = data["weather"][0]["icon"]

    # wind label
    if wind_speed < 5:
        wind_label = "Calm"
    elif wind_speed < 15:
        wind_label = "Breezy"
    elif wind_speed < 25:
        wind_label = "Windy"
    else:
        wind_label = "Very Windy"

    # sun label based on cloud cover
    if cloud_cover < 20:
        sun_label = "Sunny"
    elif cloud_cover < 50:
        sun_label = "Partly Cloudy"
    elif cloud_cover < 80:
        sun_label = "Mostly Cloudy"
    else:
        sun_label = "Overcast"

    # humidity label
    if humidity < 30:
        humidity_label = "Dry"
    elif humidity < 60:
        humidity_label = "Comfortable"
    elif humidity < 80:
        humidity_label = "Humid"
    else:
        humidity_label = "Very Humid"

    return {
        "city": data["name"],
        "country": data["sys"]["country"],
        "temp": round(temp),
        "feels_like": round(feels_like),
        "humidity": humidity,
        "humidity_label": humidity_label,
        "wind_speed": round(wind_speed),
        "wind_label": wind_label,
        "description": description.title(),
        "cloud_cover": cloud_cover,
        "sun_label": sun_label,
        "icon": icon,
        "diff": round(feels_like - temp)
    }

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/weather")
def weather():
    city = request.args.get("city", "New York")
    data = get_weather(city)
    if not data:
        return jsonify({"error": "City not found"}), 404
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
