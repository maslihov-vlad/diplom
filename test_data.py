import requests
import pymongo

# Base URL of the deployed application
base_url = 'https://web-production-b26f.up.railway.app'

# MongoDB connection string
connection_string = "mongodb+srv://maslihov22:vUEeVwpNdBz343Ti@cluster0.odsdsgy.mongodb.net/test"

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

# Add user to MongoDB
client = pymongo.MongoClient(connection_string)
db = client[database_name]
collection = db[collection_name]

user = {
    'login': 'maslo',
    'password': 'john'
}
collection.insert_one(user)

print('User added to the database.')
