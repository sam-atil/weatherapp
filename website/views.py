"""
views.py - Barebones form to request data about submitted city, state, and country
"""

from flask import Blueprint, jsonify, render_template, redirect, session, url_for
from flask import request

import os
import requests

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


#Route for the index page with form
@main_blueprint.route('/')
def index():
    #Render Form
    return render_template("index.html")

#Route to render dashboard.html
@main_blueprint.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@main_blueprint.route('/api/v1/weather', methods = ['POST'])
def get_weather():
    data = request.get_json()

    city = data.get("city")
    state = data.get("state")
    country = data.get("country")
    
    if not city or not state or not country:
        return jsonify({"error": "Missing some fields"}), 400
    
    api_key = os.getenv('WEATHER_KEY')
    api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}&units=metric")

    print(api_response.status_code)
    print(api_response.text)

    if api_response.status_code != 200: #Fail
        return jsonify({"error": "api response failure"}), 400
    
    #Temporarily storing weather
    weather_data = api_response.json()
    session["weather"] = weather_data

    return jsonify({"success": True})



@main_blueprint.route("/api/v1/display")
def latest_weather():
    weather = session.get("weather")

    if not weather:
        return jsonify({"error": "No Data to Display"}), 400
    
    return jsonify(weather)
