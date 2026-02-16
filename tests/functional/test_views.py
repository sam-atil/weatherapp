#Page Render Tests

def test_form_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/' page is requested (GET)
    THEN check if response is valid
    """

    response = test_client.get('/')
    assert response.status_code == 200
    assert b'city' in response.data
    assert b'state' in response.data
    assert b'country' in response.data

#Empty page, as we need input values to render the data elements
def test_dashboard_page(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/dashboard' page is requested (GET)
    THEN check if response is valid
    """

    response = test_client.get('/dashboard')
    assert response.status_code == 200
    assert b'weather' in response.data


#API Weather Tests
def test_weather_api(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input (POST)
    THEN check if response is valid and if session updated
    """

    #Simulating input data
    data = {
        "city": "El Paso",
        "state": "Texas",
        "country": "United States"
    }

    response = test_client.post('/api/v1/weather', json = data)

    assert response.status_code == 200
    json_data = response.get_json()
    assert response.get_json()["success"] is True

    #Check if session is updated
    with test_client.session_transaction() as session:
        assert 'weather' in session
        assert session['weather']['name'] == "El Paso"


def test_weather_api_missing_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input with missing values (POST)
    THEN check if response is valid
    """
    data = {
        "city": "El Paso",
        "state": "",
        "country": "United States"
    }

    response = test_client.post('/api/v1/weather', json = data)
    assert response.status_code == 400
    assert response.get_json()["error"] == "Missing some fields"

def test_weather_api_incorrect_fields(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/weather' route is given input with incorrect values (POST)
    THEN check if response is valid
    """
    data = {
        "city": "United States",
        "state": "United States",
        "country": "El Paso"
    }

    response = test_client.post('/api/v1/weather', json = data)
    assert response.status_code == 400
    assert response.get_json()["error"] == "api response failure"


#API Display Test

def test_display_api(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/display' route is called with weather data in session
    THEN check if response is valid
    """

    #Simulating session data
    with test_client.session_transaction() as session:
        session["weather"] = {
            "dt": 12805000000,
            "main": {"temp": 40, "feels_like": 30,"humidity": 20},
            "weather": [{"main": "Cloudy"}]
        }

    #Calling route
    response = test_client.get('/api/v1/display')  
    assert response.status_code == 200
    
    #Checking if data is returned as json
    data = response.get_json()
    assert data['dt'] == 12805000000
    assert data['main']['temp'] == 40
    assert data['main']['feels_like'] == 30
    assert data['main']['humidity'] == 20
    assert data['weather'][0]['main'] == 'Cloudy'


def test_display_api_missing_session(test_client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/api/v1/display' route is called with no weather data in session
    THEN check if response is valid
    """

    #Creating an empty session
    with test_client.session_transaction() as session:
        session.clear()  # Ensure session is empty

    #Calling route without session data
    response = test_client.get('/api/v1/display')
    assert response.status_code == 400
    assert response.get_json()['error'] == "No Data to Display"


# def test_home_page_without_login(test_client):
#     """
#     GIVEN a Flask application configured for testing, user not logged in
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'Login' in response.data
#     assert b'name' in response.data
#     assert b'password' in response.data


# def test_home_page_with_login(test_client, login_user):
#     """
#     GIVEN a Flask application configured for testing, user logged in
#     WHEN the '/' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'To-Do List' in response.data
#     assert b'Add Task' in response.data
#     assert b'Add a new task' in response.data


# def test_add_task(test_client, login_user):
#     """
#     GIVEN a Flask application configured for testing, user logged in
#     WHEN the '/add' page is posted to (POST) with a new task
#     THEN check the response is valid
#     """
#     response = test_client.post('/', data=dict(task='Test Task'), follow_redirects=True)
#     assert response.status_code == 200
#     assert b'To-Do List' in response.data
#     assert b'Add Task' in response.data
#     assert b'Add a new task' in response.data
#     assert b'Test Task' in response.data
#     assert b'not-completed' in response.data


# def test_check_task(test_client, login_user):
#     """
#     GIVEN a Flask application configured for testing, user logged in
#     WHEN the '/check/<int:task_id>' page is requested (GET)
#     THEN check the response is valid
#     """
#     response = test_client.get('/check/1', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'To-Do List' in response.data
#     assert b'Add Task' in response.data
#     assert b'Add a new task' in response.data
#     assert b'completed' in response.data

# def test_check_task_not_owner(test_client, login_user):
#     """
#     GIVEN a Flask application configured for testing, user logged in
#     WHEN the '/check/<int:task_id>' page is requested (GET) for a task not owned by the user
#     THEN check the response is valid
#     """
#     response = test_client.get('/check/2', follow_redirects=True)
#     assert response.status_code == 200
#     assert b'To-Do List' in response.data
#     assert b'Add Task' in response.data
#     assert b'Add a new task' in response.data