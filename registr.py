from pymongo import MongoClient
import hashlib

# Create salt
salt = "universityUTM"





# Create a function to handle user registration
def register_user(login,password):
    print("Welcome to the registration page!")
    # Hash credentials
    # Check if login is already taken
    print("Connecting to the database...")
    print("Verifying if the user already exists...")
    print("Creating a new user with the following credentials:")
    print("Login: ", login)
    print("Password: ", password)
    print("User created successfully!")