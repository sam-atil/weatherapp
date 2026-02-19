#Page Render Tests
def test_form_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check if response is valid
    """
    client = test_client
    response = client.get('/')

    #Checking form inputs elements
    assert response.status_code == 200
    assert b'city' in response.data
    assert b'state' in response.data
    assert b'country' in response.data

    #Checking weather container
    assert b'weather' in response.data

    #Checking established weather elements
    assert b'current-weather-val' in response.data
    assert b'weather-icon' in response.data
    assert b'temp-col' in response.data
    assert b'condition-desc' in response.data
    assert b'condition-val' in response.data
    assert b'weather-desc' in response.data
    assert b'wind-speed' in response.data
    assert b'humidity' in response.data
    assert b'visibility' in response.data
    assert b'pressure' in response.data
    assert b'dew-point' in response.data



#API Weather Tests
def test_weather_api(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input (POST)
    THEN check if response is valid and if session updated
    """

    client = test_client

    #Simulating input data
    data = {
        "city": "El Paso",
        "state": "Texas",
        "country": "United States"
    }

    response = client.post('/api/v1/weather', json = data)

    assert response.status_code == 200
    assert response.get_json()["success"] is True


def test_weather_api_missing_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input with missing values (POST)
    THEN check if response is valid
    """

    client = test_client

    data = {
        "city": "El Paso",
        "state": "",
        "country": "United States"
    }

    response = client.post('/api/v1/weather', json = data)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing some fields"

def test_weather_api_incorrect_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input with incorrect values (POST)
    THEN check if response is valid
    """

    client = test_client

    data = {
        "city": "United States",
        "state": "United States",
        "country": "El Paso"
    }

    response = client.post('/api/v1/weather', json = data)
    assert response.status_code == 400
    assert response.get_json()["error"] == "api response failure"
