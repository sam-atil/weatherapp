"""Main App file to run Weather App"""

from website import create_app

app = create_app()

"""App run condition"""
if __name__ == '__main__':
    app.run(debug=True)