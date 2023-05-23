import requests

# Gets candlestick data for a coin and timeframe from Binance API
def get_candlesticks(symbol, interval):
    """
    Gets candlestick data from Binance API.
    Returns a list of OHLCV values.
    """
    BASE_URL = "https://api.binance.com/api/v3/"

    url = BASE_URL + "klines"
    params = {
        "symbol": symbol,
        "interval": interval,
        # Max limit is 500 candles per request on Binance (change if needed)
        "limit": 500
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        candlesticks = []
        for d in data:
            candlesticks.append([
                d[0],
                float(d[1]),
                float(d[2]),
                float(d[3]),
                float(d[4]),
                float(d[5])
            ])
        return candlesticks
    else:
        # Exception handling in case of request error
        raise Exception("Request Error: %s" % response.text)


# Gets candlestick data for multiple coins and timeframes from Binance API
def get_multiple_candlesticks(symbol_interval_dict):
    """
    Gets candlestick data from Binance API for multiple symbols and intervals.
    Returns a dictionary of candlesticks {symbol: candlesticks}.
    """
    candlesticks_dict = {}
    for symbol, interval in symbol_interval_dict.items():
        candlesticks = get_candlesticks(symbol, interval)
        candlesticks_dict[symbol] = candlesticks
    return candlesticks_dict


# Collects data for multiple coins and timeframes from User
def add_coins(coin_data_list):
    coin_data = {}
    for item in coin_data_list:
        coin = item.get('symbol')
        timeframe = item.get('interval')
        coin_data[coin] = timeframe
    return coin_data
