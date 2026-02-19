"""
views.py - Barebones form to request data about submitted city, state, and country
"""

import os
from flask import Blueprint, jsonify, render_template
from flask import request

import requests

# Create a blueprint
main_blueprint = Blueprint('main', __name__)

#API Key
weather_api_key = os.getenv('WEATHER_KEY')

"""Route for the index page with form"""
@main_blueprint.route('/')
def index():
    #Render Form
    return render_template("dashboard.html")

"""Helper function to retrieve info from OpenWeather API"""
def get_weather():
    data = request.get_json()

    city = data.get("city")
    state = data.get("state")
    country = data.get("country")

    if not city or not state or not country:
        return {"error": "Missing some fields"}, 400

    try: 
        api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={weather_api_key}&units=metric")
        api_response.raise_for_status()
        weather_data = api_response.json()

    except requests.exceptions.HTTPError:
        return {"error": "api response failure"}, 400

    return {"success": True, "data": weather_data}, 200


"""API Route to return OpenWeather Data"""
@main_blueprint.route('/api/v1/weather', methods=['POST'])
def update_index():
    weather_data, status = get_weather()
    return jsonify(weather_data), status