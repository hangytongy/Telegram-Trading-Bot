from binance.client import Client
from binance.exceptions import BinanceAPIException
from datetime import datetime
import requests

def init_binance_client(api_key, api_secret):
    try:
        #client = Client(api_key, api_secret) for production
        client = Client(api_key, api_secret,testnet=True)
        return client
    except BinanceAPIException as e:
        print(f"Error initializing Binance client: {e}")
        return None

def execute_trade(client, symbol, side, quantity):
    try:
        if side.upper() == 'BUY':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_BUY,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        elif side.upper() == 'SELL':
            order = client.create_order(
                symbol=symbol,
                side=Client.SIDE_SELL,
                type=Client.ORDER_TYPE_MARKET,
                quantity=quantity
            )
        else:
            return "Invalid side. Use 'BUY' or 'SELL'."

        return f"Order executed successfully: {order}"
    except BinanceAPIException as e:
        return f"Error executing trade: {e}"

# Add more functions for other Binance operations as needed

def get_market_data(symbol):
    base_url = 'https://api.binance.com'
    endpoint = '/api/v3/ticker/24hr'
    params = {'symbol': symbol}
    depth_endpoint='/api/v3/depth'
    limit = 5
    depth_params = {'symbol': symbol, 'limit': limit}

    try:
        response = requests.get(base_url + endpoint, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        depth_response = requests.get(base_url + depth_endpoint, depth_params)
        depth_response.raise_for_status()

        data = response.json()
        price = float(data['lastPrice'])
        volume = float(data['volume'])
        timestamp = data['closeTime']  # Milliseconds timestamp
        timestamp_datetime = datetime.fromtimestamp(timestamp / 1000.0)  # Convert to seconds and to datetime
        depth_data = depth_response.json()
        bids=depth_data['bids']
        asks=depth_data['asks']
        bids_str = "\n".join([f"Price: {float(bid[0]):.2f}, Quantity: {float(bid[1]):.2f}" for bid in bids])
        asks_str = "\n".join([f"Price: {float(ask[0]):.2f}, Quantity: {float(ask[1]):.2f}" for ask in asks])

        return (f"Current price of {symbol}: {price:.2f}\n"
                f"24h Volume: {volume:.2f}\n"
                f"Order Book for {symbol}:\n"
                f"Time: {timestamp_datetime.strftime('%Y-%m-%d %H:%M:%S')}\n"
                f"\nTop {limit} Bids: \n{bids_str}\n"
                f"\nTop {limit} Asks: \n{asks_str}")
    except requests.exceptions.RequestException as e:
        return f"Error fetching market data: {e}"
