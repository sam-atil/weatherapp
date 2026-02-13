from flask import Blueprint, render_template, redirect, url_for
from flask import request

import os
import requests

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
def index():
    weather_data = None
    error_msg = None

    #User has submitted info on the form
    if request.method == 'POST':
        city = request.form.get('city')
        state = request.form.get('state')
        country = request.form.get('country')

        #Making sure neither city or country is empty
        if city and country:
            api_key = os.getenv('SECRET_KEY') #Retrieving key from environment

            #URL to retrieve weather data
            url = f"https://api.openweathermap.org/data/2.5/weather?q={city},{state},{country}&appid={api_key}&units=metric"
            response = requests.get(url)

            if response.status_code == 200:
                weather_data = response.json()
            else:
                error_msg = "Unable to fetch weather data. Please make sure you have the correct inputs"

        else:
            error_msg = "City and Country are required."

    return render_template('index.html', weather_data = weather_data, error_msg = error_msg)


# @login_required
# def todo():
#     if request.method == 'POST':
#         task = request.form['task']
#         new_task = Task(text=task, status='not-completed', user=current_user)
#         db.session.add(new_task)
#         db.session.commit()
        
#     tasks = Task.query.filter_by(user=current_user).all()
#     return render_template('todo.html', tasks=tasks)


# @main_blueprint.route('/check/<int:task_id>')
# @login_required
# def check(task_id):
#     task = Task.query.get(task_id)
    
#     if not task or task.user != current_user:
#         return redirect(url_for('main.todo'))
    
#     task.status = 'completed'
#     db.session.commit()

#     return redirect(url_for('main.todo'))



# @main_blueprint.route('/conditional')
# def conditional():
#     user = 'admin'
#     return render_template('conditional.html', user=user)


# @main_blueprint.route('/loop')
# def loop():
#     users = ['admin', 'user', 'guest']
#     return render_template('loop.html', items=users)


# @main_blueprint.route('/form', methods=['GET', 'POST'])
# def form():
#     if request.method == 'POST':
#         username = request.form['username']
#         password = request.form['password']
#         return f'Logged in as {username}'
    
#     return render_template('form.html')