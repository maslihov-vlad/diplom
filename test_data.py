import requests

# Base URL of the deployed application
base_url = 'https://web-production-b26f.up.railway.app'


# MongoDB database and collection names
database_name = "test"
collection_name = "users"

# Test the /hello endpoint
hello_url = f'{base_url}/hello'
hello_response = requests.get(hello_url)
if hello_response.status_code == 200:
    hello_data = hello_response.json()
    print(hello_data['message'])
else:
    print('Failed to retrieve data from /hello endpoint')

# Test the /name endpoint
name_url = f'{base_url}/name'
name_data = {'name': 'John'}
name_response = requests.post(name_url, json=name_data)
if name_response.status_code == 200:
    name_data = name_response.json()
    print(name_data['message'])
else:
    print('Failed to retrieve data from /name endpoint')



print('User added to the database.')
