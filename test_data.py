import requests
#from test2 import check_name
import time
# Set the base URL for the API endpoints
base_url = 'https://web-production-b26f.up.railway.app/api'

# Register a new user
def register_user(login, password):
    endpoint = f'{base_url}/register'
    headers = {'Content-Type': 'application/json'}
    data = {
        'login': login,
        'password': password
    }
    response = requests.post(endpoint, json=data, headers=headers)
    print(response.json())

# Login and obtain an access token
def login_user(login, password):
    endpoint = f'{base_url}/login'
    headers = {'Content-Type': 'application/json'}
    data = {
        'login': login,
        'password': password
    }
    response = requests.post(endpoint, json=data,headers=headers )
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        return access_token
    else:
        print(response.json())

# Access protected endpoint
def access_protected(token):
    # Set the headers with the JWT token
    headers = {'Authorization': f'Bearer {token}'}
    # Send the GET request to the protected endpoint
    response = requests.get(f'{base_url}/protected', headers=headers)
    # Check the response status code
    if response.status_code == 200:
        # Print the response content
        print(response.json())
    else:
        # Print the error message
        print(response.content)

def access_app(token):
    endpoint = 'https://web-production-b26f.up.railway.app/app'
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
    response = requests.get(endpoint, headers=headers, json=data)
    print(response.status_code)
    print(response.json())

login = "masla"
password = "sos"
# Test the endpoints
register_user(login, password)
print('Used credentials:', login, password)
token = login_user(login, password)
print("Logged in successfully!")
print("Login:", login)
print("Password:", password)
print("Token:", token)
access_protected(token)
access_app(token)
