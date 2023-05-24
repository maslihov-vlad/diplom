from pymongo import MongoClient
import hashlib

# Create salt
salt = "universityUTM"

# Connect to the MongoDB server
client = MongoClient('mongodb+srv://maslihov22:vUEeVwpNdBz343Ti@cluster0.odsdsgy.mongodb.net/')

# Access the database and collection
db = client['test']
collection = db['users']


# Create a function to handle user registration
def register_user(login,password):
    print("Welcome to the registration page!")
    # Hash credentials
    password_hash = hashlib.sha256(password.encode() + salt.encode()).hexdigest()
    # Check if login is already taken
    print("Connecting to the database...")
    existing_user = collection.find_one({"login": login})
    if existing_user:
        return False
    else:
        # Create a dictionary with user data
        user_data = {
            "login": login,
            "password": password_hash
        }
        # Insert the user data into the collection
        collection.insert_one(user_data)
        return True