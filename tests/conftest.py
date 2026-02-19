"""Testing file for the whole program"""

import os
import sys
import pytest
from website import create_app
sys.path.append(os.path.dirname(os.path.dirname(__file__)))#Forcing 

@pytest.fixture(scope='module')
def test_client():
    """Set the Testing configuration prior to creating the Flask application"""
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    flask_app = create_app()

    # Create a test client using the Flask application configured for testing
    with flask_app.test_client() as test_client:
        yield test_client # this is where the testing happens!