import json
from typing import Dict, Tuple
from utils import request

'''
Returns the asset information for the given symbol.
'a' -> Ask
'b' -> Bid
'c' -> Close
'v' -> Volume
'''
def retrieve_asset_info(symbol: str) -> Tuple[Dict, Dict]:
    response = request(
        method="GET", 
        path="/0/public/Ticker",
        query={'pair': f'{symbol}USD'}
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200 or ('error' in json_data and len(json_data['error'])):
        return None, json_data['error']

    result = json_data['result']
    values = list(result.values())

    return values[0], None

def retreive_asset_pair_name(symbol1: str, symbol2: str) -> Tuple[Dict, Dict]:
    response = request(
        method="GET", 
        path="/0/public/AssetPairs",
        query={'pair': f'{symbol1}/{symbol2}'}
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200 or not 'result' in json_data:
        return None, json_data['error']

    result = json_data['result']

    return result, None

def retrieve_trades_history() -> Tuple[Dict, Dict]:
    response = request(
        method="POST", 
        path="/0/private/TradesHistory"
    )
    
    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200:
        return None, json_data['error']

    result = json_data['result']
    trades = {}

    for trade in result['trades'].values():
        trades[trade['pair']] = {
            'pair': trade['pair'],
            'time': trade['time'],
            'type': trade['type'],
            'amount': float(trade['vol']),
            'price': float(trade['price']),
            'cost': float(trade['cost']),
            'fee': float(trade['fee']),
            'margin': float(trade['margin']),
        }

    return trades, None

def retrieve_portfolio() -> Tuple[Dict, Dict]:
    response = request(
        method="POST", 
        path="/0/private/Balance"
    )
    
    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200:
        return None, json_data['error']
        
    result = json_data['result']
    portfolio = []

    trades, error = retrieve_trades_history()

    if error:
        return None, error

    total_loss_for_all_assets = 0

    for symbol in result.keys():
        asset_info, error = retrieve_asset_info(symbol)
        history = trades.get(f'{symbol}USD', None)

        if error or float(result[symbol]) == 0.00:
            continue
        
        current_loss = (float(asset_info['c'][0]) - history['price']) * history['amount'] if history is not None else 0
        total_loss_for_all_assets += current_loss

        asset_data = {
            'symbol': symbol,
            'amount': float(result[symbol]),
            'profit_loss': current_loss,
            'price': float(asset_info['c'][0]),
            'value': float(result[symbol]) * float(asset_info['c'][0])
        }

        portfolio.append(asset_data)

    data = {
        'positions': portfolio,
        'total_profit_loss': total_loss_for_all_assets,
    }

    return data, None

def execute_buy_order(symbol: str, amount: float, quote_currency: str = 'USD') -> Tuple[Dict, Dict]:
    body = {
        'ordertype': 'market', #change later
        'type': 'buy',
        'volume': amount, #change later
        'pair': f'{symbol}/{quote_currency}'    
    }

    response = request(
        method="POST", 
        path="/0/private/AddOrder",
        body=body
    )

    response_data = response.read().decode('utf-8')
    json_data = json.loads(response_data)

    if 'error' in json_data:
        return None, json_data['error']

    return json_data['result'], None