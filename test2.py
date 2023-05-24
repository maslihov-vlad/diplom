import requests

def register_user(login, password):
    endpoint = 'https://web-production-b26f.up.railway.app/api/register'
    headers = {'Content-Type': 'application/json'}
    data = {
        'login': login,
        'password': password
    }
    response = requests.post(endpoint, json=data, headers=headers)
    if response.status_code == 200:
        try:
            print("Registration successful!")
            print(response.text)
        except ValueError:
            print("Registration failed! Response content is not valid JSON.")
    else:
        print("Registration failed!")
        print(response.text)

# Provide the username and password for registration
login = 'maslo'
password = 'sos'

# Test the registration endpoint
register_user(login, password)
