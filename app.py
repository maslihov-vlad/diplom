from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from flask_jwt_extended import exceptions
import jwt as j
from registr import collection
from registr import register_user
from login import login_user
from candlesticks_get import add_coins
from strategies import rsi_strategy, bollinger_bands_strategy, moving_average_crossover_strategy, macd_strategy



app = Flask(__name__)
CORS(app)
app.config['JWT_SECRET_KEY'] = 'secret'
jwt = JWTManager(app)


@app.route('/hello', methods=['GET'])
def index():
    return jsonify({'message': 'Hello, Maslo!'}), 200


@app.route('/name', methods=['POST'])
def name():
    data = request.get_json()
    name = data['name']
    return jsonify({'message': f'Hello, {name}!'}), 200

#Create a login endpoint that checks the user's credentials and returns a JWT:
@app.route('/api/login', methods=['POST'])
def login_endpoint():
    data = request.get_json()
    login = data['login']
    password = data['password']
    logged = login_user(login, password)
    # Check the user's credentials by querying the database
    if logged:
        # Generate a JWT and return it to the client
        access_token = create_access_token(identity=login)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/register', methods=['POST'])
def register_endpoint():
    data = request.get_json()
    login = data['login']
    password = data['password']
    register_user()
    return jsonify({'message': 'User registered successfully!'}), 200



@app.route('/api/protected', methods=['GET'])
@jwt_required()
def protected():
    # Get the user's identity from the JWT
    identity = get_jwt_identity()
    return jsonify({'message': f'Hello, {identity}!'}), 200



# Endpoint for app functions
@app.route('/app', methods=['GET'])
def app_functions():
    token = request.headers.get('Authorization')
    token_nice = str.replace(str(token), 'Bearer ', '')
    if not token:
        return jsonify({"message": "Authorization token not found"}), 401

    try:
        #decode the token
        decoded_token = j.decode(token_nice, app.config['JWT_SECRET_KEY'], algorithms=['HS256'])
        
    #Except in case of invalid token
    except exceptions.JWTDecodeError:
        return jsonify({"message": "Invalid token"}), 401
    
    
    login = decoded_token['sub']
    user = collection.find_one({"login": login})
    if not user:
        return jsonify({"message": "User not found"}), 401

    # Get the coins and time frames data from the request
    data = request.get_json()
    coin_data_list = data.get('coins')
    
    # Call the add_coins function with the coin and time frame data
    coins_dict = add_coins(coin_data_list)
    
    # fast and slow period for moving average
    fast = 10
    slow = 20
    # window size and number of standard deviation
    window_size = 20
    num_std_dev = 2
    signals = []
    
    # loop through the coins dictionary and get the signals
    for symbol, interval in coins_dict.items():
        signal_ma = moving_average_crossover_strategy(
            symbol, interval, fast, slow)
        signal_BB = bollinger_bands_strategy(
            symbol, interval, window_size, num_std_dev)
        signal_RSI = rsi_strategy(symbol, interval, window_size, num_std_dev)
        signal_MACD = macd_strategy(symbol, interval)
        signal_data = {
            'symbol': symbol,
            'interval': interval,
            'MA': signal_ma,
            'BB': signal_BB,
            'RSI': signal_RSI,
            'MACD': signal_MACD
        }
        signals.append(signal_data)
        
    # Return the signals to the user
    return jsonify({"signals": signals}), 200

if __name__ == '__main__':
    app.run()



# TODO

# 1. add more strategies (optional)
# 2. add register and login DONE
# 3. add database DONE
# 4. add hashing DONE
# 5. Create endpoints Done
# 6. Connect to frontend

