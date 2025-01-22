from binance.client import Client
from binance.exceptions import BinanceAPIException
import os
from dotenv import load_dotenv

load_dotenv()

# Replace these with your API key and secret
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

def test_futures_account():
    """
    Tests if the Binance Futures account is usable by retrieving account balance.
    :return: None
    """
    try:
        # Initialize Binance client
        client = Client(API_KEY, API_SECRET)
        #client.FUTURES_URL = "https://fapi.binance.com"
        
        # Test connectivity and time synchronization
        client.futures_ping()
        print("Ping successful. API connection is active.")
        
        # Fetch account information
        account_info = client.futures_account_balance()
        
        # Display balances
        if account_info:
            print("Futures Account Balance:")
            for balance in account_info:
                print(f"Asset: {balance['asset']}, Wallet Balance: {balance['balance']}, "
                      f"Available Balance: {balance['withdrawAvailable']}")
        else:
            print("No balance found in the Futures account.")
        
    except BinanceAPIException as e:
        print(f"Binance API Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the test
test_futures_account()
