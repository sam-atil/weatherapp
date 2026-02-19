"""
views.py - Barebones form to request data about submitted city, state, and country
"""

import os
from flask import Blueprint, jsonify, render_template
from flask import request
import requests
from website.views import main_blueprint

#API Key
weather_api_key = os.getenv('WEATHER_KEY')


@main_blueprint.route('/')
def index():
    """Route for the index page with form"""
    #Render Form
    return render_template("dashboard.html")

def get_weather():
    """Helper function to retrieve info from OpenWeather API"""
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



@main_blueprint.route('/api/v1/weather', methods=['POST'])
def update_index():
    """API Route to return OpenWeather Data"""
    weather_data, status = get_weather()
    return jsonify(weather_data), status