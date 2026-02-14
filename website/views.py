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
    
    if not city or not country:
        return jsonify({"error": "Missing some fields"}), 400
    
    api_key = os.getenv('WEATHER_KEY')
    api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}&units=metric")

    print(api_response.status_code)
    print(api_response.text)

    if api_response.status_code != 200: #Fail
        return jsonify({"error": "api response failure"})
    
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
    # weather_data = None

    # if request.method == 'POST':
    #     data = request.json
    #     city = data.get('city_name')
    #     state = data.get('state_name')
    #     country = data.get('country_name')
    
    #     if city and state and country: #input fields aren't empty
    #         api_key = os.getenv('SECRET_KEY')
    #         api_response = requests.get(f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}&units=metric")
    #         print(api_response.text)
    #         if api_response.status_code == 200: #Success
    #             weather_data = api_response.json()

    #     #cleaning json
                

    # return jsonify(weather_data)


# #index.html page
# @main_blueprint.route('/', methods=['GET', 'POST'])
# def index():
#     weather_data = None
#     error_msg = None

#     #User has submitted info on the form
#     if request.method == 'POST':
#         city = request.form['city']
#         state = request.form['state']
#         country = request.form['country']

#         #Making sure neither city or country is empty
#         if city and country:
#             api_key = os.getenv('SECRET_KEY') #Retrieving key from environment

#             #URL to retrieve weather data
#             url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}&units=metric"
#             response = requests.get(url)

#             if response.status_code == 200:
#                 weather_data = response.json()
#                 #render bootstrap.html to send user to this page
#                 return render_template('dashboard.html', weather_data = weather_data, error_msg = error_msg)
#             else:
#                 error_msg = "Unable to fetch weather data. Please make sure you have the correct inputs"

#         else:
#             error_msg = "City and Country are required."

#     return render_template('index.html', weather_data = weather_data, error_msg = error_msg)


# @main_blueprint.route('/api/v1/weather', methods=['GET'])
# def api_weather_dashboard():
    

# # @login_required
# # def todo():
# #     if request.method == 'POST':
# #         task = request.form['task']
# #         new_task = Task(text=task, status='not-completed', user=current_user)
# #         db.session.add(new_task)
# #         db.session.commit()
        
# #     tasks = Task.query.filter_by(user=current_user).all()
# #     return render_template('todo.html', tasks=tasks)


# # @main_blueprint.route('/check/<int:task_id>')
# # @login_required
# # def check(task_id):
# #     task = Task.query.get(task_id)
    
# #     if not task or task.user != current_user:
# #         return redirect(url_for('main.todo'))
    
# #     task.status = 'completed'
# #     db.session.commit()

# #     return redirect(url_for('main.todo'))



# # @main_blueprint.route('/conditional')
# # def conditional():
# #     user = 'admin'
# #     return render_template('conditional.html', user=user)


# # @main_blueprint.route('/loop')
# # def loop():
# #     users = ['admin', 'user', 'guest']
# #     return render_template('loop.html', items=users)


# # @main_blueprint.route('/form', methods=['GET', 'POST'])
# # def form():
# #     if request.method == 'POST':
# #         username = request.form['username']
# #         password = request.form['password']
# #         return f'Logged in as {username}'
    
# #     return render_template('form.html')