from pymongo import MongoClient
import hashlib

# Create salt
salt = "universityUTM"

# Connect to the MongoDB server
client = MongoClient('mongodb://localhost:27017/')

# Access the database and collection
db = client['app']
collection = db['registration']


# Create a function to handle user registration
def register_user(login,password):

    print("Welcome to the registration page!")

    # Hash credentials
    password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()

    # Check if login is already taken
    existing_user = collection.find_one({"login": login})
    if existing_user:
        return False
    else:
        # Create a dictionary with user data
        user_data = {
            "login": login,
            "password": password
        }
        
        # Insert the user data into the collection
        collection.insert_one(user_data)
        return True