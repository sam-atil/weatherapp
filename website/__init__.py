# from views import main_blueprint
# from auth import auth_blueprint
import os

from dotenv import \
    load_dotenv  # Works for local server, needs .env file to work
from flask import Flask
# from models import db, User
from flask_login import LoginManager

load_dotenv()


def create_app():
    app = Flask(__name__)

    # check if testing app, to configure the app for testing
    if os.environ.get('CONFIG_TYPE') == 'config.TestingConfig':
        app.config['SECRET_KEY'] = 'secret'
    else:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') #within .env file
        

    from .views import main_blueprint

    # Register blueprint for routes
    app.register_blueprint(main_blueprint)

    #if __name__ == '__main__':
    with app.app_context():
        print('Creating index page')
        #app.run(debug=True)

    return app


if __name__ == '__main__':
    create_app()