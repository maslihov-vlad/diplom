# Description: Contains trading strategies for binance.
from candlesticks_get import get_candlesticks
import pandas as pd

# moving average crossover strategy for binance
def moving_average_crossover_strategy(symbol, interval, fast_period, slow_period):
    """
    Strategy: Moving Average Crossover.
    Returns signal to buy (Long) or sell (Short) based on price data.
    """
    # Get candlesticks for symbol and interval
    candlesticks = get_candlesticks(symbol, interval)

    # Calculate moving averages
    close_prices = [c[4] for c in candlesticks]
    fast_ma = sum(close_prices[-fast_period:]) / fast_period
    slow_ma = sum(close_prices[-slow_period:]) / slow_period

    # Determine signal
    if fast_ma > slow_ma:
        return "Long"
    else:
        return "Short"

# bollinger bands strategy for binance


def bollinger_bands_strategy(symbol, interval, window_size, num_std_dev):
    """
    Strategy: Bollinger Bands.
    Returns signal to buy (Long) or sell (Short) based on price data.
    """
    # Get candlesticks for symbol and interval
    df = pd.DataFrame(get_candlesticks(symbol, interval))
    df = df.iloc[:, :6]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index, unit='ms')

    # Calculate rolling mean and standard deviation
    rolling_mean = df['close'].rolling(window_size).mean()
    rolling_std = df['close'].rolling(window_size).std()

    # Calculate upper and lower bands
    upper_band = rolling_mean + (rolling_std * num_std_dev)
    lower_band = rolling_mean - (rolling_std * num_std_dev)

    # Check if last price is above upper band or below lower band
    for i in range(1, len(df)):
        if df['close'][i-1] <= lower_band[i-1] and df['close'][i] > lower_band[i]:
            return 'Long'
        elif df['close'][i-1] >= upper_band[i-1] and df['close'][i] < upper_band[i]:
            return 'Short'
    return 'Hold'

# RSI strategy for binance

def rsi_strategy(symbol, interval, window_size, num_std_dev):
    """
    Strategy: RSI.
    Returns signal to buy (Long) or sell (Short) based on price data.
    """
    # Get candlesticks for symbol and interval
    df = pd.DataFrame(get_candlesticks(symbol, interval))
    df = df.iloc[:, :6]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index, unit='ms')

    # Calculate RSI
    delta = df['close'].diff()
    gain = delta.mask(delta < 0, 0)
    loss = -delta.mask(delta > 0, 0)
    avg_gain = gain.rolling(window_size).mean()
    avg_loss = loss.rolling(window_size).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    # Generate signal based on RSI
    signal = pd.Series(index=rsi.index)
    # Long signal when RSI crosses below oversold threshold
    signal[rsi < (30 - num_std_dev)] = 'Long'
    # Short signal when RSI crosses above overbought threshold
    signal[rsi > (70 + num_std_dev)] = 'Short'
    # Return the first valid signal value (Long or Short) as the strategy signal
    if signal.isin(['Long']).any():
        return 'Long'
    elif signal.isin(['Short']).any():
        return 'Short'

# MACD strategy for binance
def macd_strategy(symbol, interval):
    """
    Strategy: MACD.
    Returns signal to buy (Long) or sell (Short) based on price data.
    """
    # Get candlesticks for symbol and interval
    df = pd.DataFrame(get_candlesticks(symbol, interval))
    df = df.iloc[:, :6]
    df.columns = ['time', 'open', 'high', 'low', 'close', 'volume']
    df = df.set_index('time')
    df.index = pd.to_datetime(df.index, unit='ms')

    # Calculate MACD
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal_line = macd.ewm(span=9, adjust=False).mean()

    
    # Long signal when MACD line crosses above signal line
    if (macd > signal_line).any():
        return 'Long'

    # Short signal when MACD line crosses below signal line
    elif (macd < signal_line).any():
        return 'Short'


