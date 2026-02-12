from flask import Blueprint, render_template, redirect, url_for
from flask import request
from flask_login import login_required, current_user

# Create a blueprint
main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/', methods=['GET', 'POST'])
@login_required
def todo():
    if request.method == 'POST':
        task = request.form['task']
        new_task = Task(text=task, status='not-completed', user=current_user)
        db.session.add(new_task)
        db.session.commit()
        
    tasks = Task.query.filter_by(user=current_user).all()
    return render_template('todo.html', tasks=tasks)


@main_blueprint.route('/check/<int:task_id>')
@login_required
def check(task_id):
    task = Task.query.get(task_id)
    
    if not task or task.user != current_user:
        return redirect(url_for('main.todo'))
    
    task.status = 'completed'
    db.session.commit()

    return redirect(url_for('main.todo'))



@main_blueprint.route('/conditional')
def conditional():
    user = 'admin'
    return render_template('conditional.html', user=user)


@main_blueprint.route('/loop')
def loop():
    users = ['admin', 'user', 'guest']
    return render_template('loop.html', items=users)


@main_blueprint.route('/form', methods=['GET', 'POST'])
def form():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        return f'Logged in as {username}'
    
    return render_template('form.html')