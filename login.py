from pymongo import MongoClient
import hashlib

#Create salt
salt = "universityUTM"

# Connect to the MongoDB server
# Connect to the MongoDB server
connectionString = "mongodb+srv://maslihov22:vUEeVwpNdBz343Ti@cluster0.odsdsgy.mongodb.net/"
client = MongoClient(connectionString)
# Access the database and collection
db = client['test']
collection = db['users']


def login_user(login, password):
    print("Welcome to the login page!")
    # Hash credentials
    password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
    # Check if user is registered
    user = collection.find_one({"login": login, "password": password_hash})
    if user:
        print("Welcome to the app!")
        return True
    else:
        print("User not found!")
        print("Please register first or check your credentials!")
        return False