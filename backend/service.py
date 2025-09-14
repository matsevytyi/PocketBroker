from collections import defaultdict
import json
from typing import Dict, Optional, Tuple, List
from utils import request
from pprint import pprint
from data import TICKER_MAPPINGS

'''
Returns the asset information for the given symbol.
'a' -> Ask
'b' -> Bid
'c' -> Close
'v' -> Volume
'''

def retrieve_asset_info(pair: str) -> Tuple[Dict, Dict]:
    response = request(
        method="GET", 
        path="/0/public/Ticker",
        query={'pair': pair}
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200 or ('error' in json_data and len(json_data['error'])):
        return None, json_data['error']

    result = json_data['result']
    return result, None

def retrieve_asset_pair_name(symbol1: str, symbol2: str) -> Tuple[Dict, Dict]:
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
    trades = defaultdict(list)

    for trade in result['trades'].values():
        if trade['type'] == 'sell':
            if trade['pair'] in trades:
                trades[trade['pair']] = []
            continue

        trades[trade['pair']].append({
            'pair': trade['pair'],
            'time': trade['time'],
            'type': trade['type'],
            'amount': float(trade['vol']),
            'price': float(trade['price']),
            'cost': float(trade['cost']),
            'fee': float(trade['fee']),
            'margin': float(trade['margin']),
        })

    return trades, None

def compute_asset_profit_loss(current: float, trades: List[Dict]) -> float:
    total = 0
    for trade in trades:
        total += trade['cost']

    return current - total

def get_kraken_ticker_pair(symbol: str) -> str:
    symbol = symbol.upper()
    
    for internal_name, mapping_info in TICKER_MAPPINGS.items():
        if symbol in mapping_info['kraken_ticker']:
            for pair in mapping_info["kraken_fiat_pairs"]:
                if "USD" in pair:
                    return pair
            
    return None

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
    print(result)

    portfolio = []

    trades, error = retrieve_trades_history()

    if error:
        return None, error

    total_loss_for_all_assets = 0

    assets = {}

    asset_symbols = ""
    equivalents = {}
    for symbol in result.keys():
        kraken_ticker_pair = get_kraken_ticker_pair(symbol)

        if kraken_ticker_pair is None:
            continue

        equivalents[symbol] = kraken_ticker_pair
        asset_symbols += kraken_ticker_pair + ","

    asset_symbols = asset_symbols[:-1]

    assets_info, error = retrieve_asset_info(asset_symbols.encode())

    if error:
        return None, error

    for pair, info in assets_info.items():
        assets[pair] = info

    for ticker, pair in equivalents.items():
        history = trades.get(pair)

        if float(result[ticker]) == 0.00:
            continue

        asset_value = float(result[ticker]) * float(assets[pair]['c'][0])
        
        current_loss = compute_asset_profit_loss(asset_value, history) if history else 0
        total_loss_for_all_assets += current_loss

        asset_data = {
            'symbol': ticker,
            'holding_amount': float(result[ticker]),
            'profit_loss': current_loss,
            'price': float(assets[pair]['c'][0]),
            'value': asset_value
        }

        portfolio.append(asset_data)

    data = {
        'positions': portfolio,
        'total_profit_loss': total_loss_for_all_assets,
    }

    return data, None

def execute_buy_order(pair: str, amount: float, order_type: str = 'market', price: Optional[float] = None) -> Tuple[Dict, Dict]:
    body = {
        'ordertype': order_type,
        'type': 'buy',
        'volume': amount,
        'pair': pair    
    }

    if order_type == 'limit':
        if not price:
            return None, 'Price is required for limit orders'

        body['price'] = price

    response = request(
        method="POST", 
        path="/0/private/AddOrder",
        body=body
    )

    response_data = response.read().decode('utf-8')
    json_data = json.loads(response_data)

    if 'error' in json_data and len(json_data['error']):
        return None, json_data['error']

    return json_data['result'], None

def execute_sell_order(pair: str, amount: float, order_type: str = 'market', price: Optional[float] = None) -> Tuple[Dict, Dict]:
    body = {
        'ordertype': order_type,
        'type': 'sell',
        'volume': amount,
        'pair': pair
    }

    if order_type == 'limit':
        if not price:
            return None, 'Price is required for limit orders'

        body['price'] = price

    response = request(
        method="POST", 
        path="/0/private/AddOrder",
        body=body
    )

    response_data = response.read().decode('utf-8')
    json_data = json.loads(response_data)

    if 'error' in json_data and len(json_data['error']):
        return None, json_data['error']

    return json_data['result'], None