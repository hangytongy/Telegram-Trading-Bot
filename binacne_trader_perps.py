import decimal
from binance.client import Client
from binance.enums import *
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
    
def get_current_positions_formatted(api_key, api_secret):

    client = Client(api_key, api_secret)
    try:
        # Fetch all position information
        positions = client.futures_position_information()
        balances = client.futures_account_balance()
        
        # Filter positions with a non-zero position amount
        open_positions = [
            {
                "symbol": position["symbol"],
                "positionAmt": float(position["positionAmt"]),
                "entryPrice": float(position["entryPrice"]),
                "unrealizedPnL": float(position["unrealizedProfit"]),
                "leverage": int(position["leverage"]),
                "marginType": position["marginType"],
                "side": "LONG" if float(position["positionAmt"]) > 0 else "SHORT",
            }
            for position in positions
            if float(position["positionAmt"]) != 0
        ]
        
        # Format the positions as a string
        if open_positions:
            position_strings = []
            for pos in open_positions:
                position_strings.append(
                    f"Symbol: {pos['symbol']}\n"
                    f"Side: {pos['side']}\n"
                    f"Quantity: {pos['positionAmt']}\n"
                    f"Entry Price: {pos['entryPrice']}\n"
                    f"Unrealized PnL: {pos['unrealizedPnL']}\n"
                    f"Leverage: {pos['leverage']}\n"
                    f"Margin Type: {pos['marginType']}\n"
                    f"--------------------"
                )
            positions_text = "\n".join(position_strings)
        else:
            positions_text = "No open positions."

        # Format balance
        balance_strings = []
        for balance in balances:
            asset = balance["asset"]
            wallet_balance = float(balance["balance"])
            available_balance = float(balance["withdrawAvailable"])
            balance_strings.append(
                f"Asset: {asset}\n"
                f"Wallet Balance: {wallet_balance}\n"
                f"Available Balance: {available_balance}\n"
                f"--------------------"
            )
        balances_text = "\n".join(balance_strings)
        
        return f"Open Positions:\n{positions_text}\n\nAccount Balances:\n{balances_text}"

    except Exception as e:
        return f"Error retrieving positions: {e}"

def execute_market(api_key, api_secret, symbol, side, quantity):

    if str(side).upper() == "BUY":
        side = SIDE_BUY
    else:
        side = SIDE_SELL
    
    try:
        client = Client(api_key, api_secret)
        if client:
            order = client.futures_create_order(
                symbol = symbol,
                side=side,
                type = FUTURE_ORDER_TYPE_MARKET,
                quantity=quantity
            )
            return ("Market order placed:", order)
        else:
            return('Failed to initialize Binance client. Please check your API key and secret.')


        return f"Order executed successfully: {order}"
    except Exception as e:
        return f"Error executing trade: {e}"
    
def place_limit_order(api_key, api_secret,symbol, quantity, price, side, time_in_force="GTC"):

    if str(side).upper() == "BUY":
        side = SIDE_BUY
    else:
        side = SIDE_SELL

    client = Client(api_key, api_secret)
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type=FUTURE_ORDER_TYPE_LIMIT,
            timeInForce=time_in_force,
            quantity=quantity,
            price=price
        )
        return f"Limit order placed successfully:\n{order}"
    except Exception as e:
        return f"Error placing limit order: {e}"


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
    

    
