import requests
import json

# Set the base URL for the API endpoints
base_url = 'http://localhost:5000/api'
base_url_2 = 'http://maslosos.pythonanywhere.com/api'
# Register a new user
def register_user(login, password):
    endpoint = f'{base_url_2}/register'
    data = {
        'login': login,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    print(response.json())

# Login and obtain an access token
def login_user(login, password):
    endpoint = f'{base_url_2}/login'
    data = {
        'login': login,
        'password': password
    }
    response = requests.post(endpoint, json=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(response.json())

# Access protected endpoint
def access_protected(token):
        # Set the base URL
    base_url = 'http://localhost:5000'
    base_url_2 = 'http://maslosos.pythonanywhere.com/'
    # Set the headers with the JWT token
    headers = {'Authorization': f'Bearer {token}'}
    # Send the GET request to the protected endpoint
    response = requests.get(f'{base_url_2}/api/protected', headers=headers)
    # Check the response status code
    if response.status_code == 200:
        # Print the response content
        print(response.json())
    else:
        # Print the error message
        print(response.content)

def access_app(token):
    endpoint = 'http://localhost:5000/app'
    endpoint_2 = 'http://maslosos.pythonanywhere.com//app'
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        'coins': [
            {'symbol': 'BTCUSDT', 'interval': '1h'},
            {'symbol': 'ETHUSDT', 'interval': '1h'}
        ]
    }
    response = requests.get(endpoint_2, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

login = "masla"
password = "sos"
# Test the endpoints
register_user(login, password)
print('Used credentials: ', login," ", password)
token = login_user(login, password)
print("Logged in successfully!")
print("Login", login)
print("Password", password)
print("Token", token)
access_protected(token)
access_app(token)
