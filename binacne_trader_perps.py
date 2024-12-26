import decimal
from binance.client import Client
from binance.error import ParameterRequiredError
from datetime import datetime,timedelta
import requests
import pandas as pd 

def init_binance_client(api_key, api_secret):
    try:
        #client = Client(api_key, api_secret) for production
        client = Client(api_key, api_secret)
        return client
    except Exception as e:
        print(f"Error initializing Binance client: {e}")
        return None

def execute_stop_loss(api_key, api_secret, symbol, time_in_force, stop_price, quantity, side):
    try:
        client = Client(api_key, api_secret)
        if client:
            print('client ok')
            params = {
                'symbol': symbol,
                'side': side.upper(),
                'type': 'STOP_LOSS',
                'timeInForce': time_in_force,
                'quantity': quantity,
                'stopPrice': stop_price
            }
            
            response = client.create_order(**params)
            return response
        else:
            return 'Failed to initialize Binance client. Please check your API key and secret.'
            
    except Exception as e:
        return f"An error occurred placing stop loss order: {str(e)}"
