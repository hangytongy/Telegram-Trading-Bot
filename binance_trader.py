from binance.spot import Spot as Client
from binance.error import ParameterRequiredError
from datetime import datetime,timedelta
import requests

def init_binance_client(api_key, api_secret):
    try:
        #client = Client(api_key, api_secret) for production
        client = Client(api_key, api_secret,base_url='https://testnet.binance.vision')
        return client
    except Exception as e:
        print(f"Error initializing Binance client: {e}")
        return None

def execute_limit(api_key, api_secret, symbol, side, price, quantity):
    try:
        client = Client(api_key, api_secret,base_url='https://testnet.binance.vision')
        if client:
            params = {
                    'symbol': symbol,
                    'side': side.upper(),
                    'type': 'LIMIT',
                    'quantity' : quantity,
                    'price': price
                    }
            print(params)
            response = client.new_order(**params)
            return response
        else:
            return('Failed to initialize Binance client. Please check your API key and secret.')


        return f"Order executed successfully: {order}"
    except Exception as e:
        return f"Error executing trade: {e}"

def execute_market(api_key, api_secret, symbol, side, quantity):
    try:
        client = Client(api_key, api_secret,base_url='https://testnet.binance.vision')
        if client:
            params = {
                    'symbol': symbol,
                    'side': side.upper(),
                    'type': 'MARKET',
                    'quantity' : quantity,
                    }
            print(params)
            response = client.new_order(**params)
            return response
        else:
            return('Failed to initialize Binance client. Please check your API key and secret.')


        return f"Order executed successfully: {order}"
    except Exception as e:
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

def get_balance(api_key, api_secret):
    try:
        client = Client(api_key, api_secret,base_url='https://testnet.binance.vision')
        print("get blanace, client ok")
        if client:
            info = client.account()
            balances = info['balances']

            messages = []
            current_message = ''
            for balance in balances:
                asset = balance['asset']
                free_balance = float(balance['free'])
                locked_balance = float(balance['locked'])

                if free_balance > 0 or locked_balance > 0:
                    balance_line = f"Asset: {asset}, Free: {free_balance:.2f}, Locked: {locked_balance:.2f}\n"
        
                if len(current_message) + len(balance_line) > 4096:
                    messages.append(current_message.strip())  # Add the current chunk to the list
                    current_message = balance_line  # Start a new message with the current line
                else:
                    # Otherwise, add the line to the current message
                    current_message += balance_line
                
             # Append the last accumulated message (if any)
            if current_message:
                messages.append(current_message.strip())
            return messages

            if len(messages) == 0:
                return('No balance in account.')

        else:
            return('Failed to initialize Binance client. Please check your API key and secret.')
        
    except Exception as e:
        return f"Failed to retrieve balance: {str(e)}"

def get_margin(api_key, api_secret):
    current_time = datetime.now()
    date_30_days_ago = current_time - timedelta(days=30)

    current_time = int(current_time.timestamp()*1000)
    date_30_days_ago = int(date_30_days_ago.timestamp()*1000)
    params = {
        'asset' : 'USDT',
        'size' : 90,
        'startTime' : date_30_days_ago,
        'endTime' : current_time,
        'recvWindow': 20000,
        "timestamp": current_time
    }

    try:
        client = Client(api_key, api_secret)
        if client:
            response = client.margin_interest_rate_history(**params)
            return response[:3]
        else:
            return f"where tf is the client"

    except Exception as e:
        return f"error {e}"
