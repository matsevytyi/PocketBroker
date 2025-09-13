import os
from dotenv import load_dotenv
import http.client
import urllib.request
import urllib.parse
import json
from utils import get_signature, get_nonce
from typing import Dict, Optional, Tuple

load_dotenv()

KRAKEN_API_KEY = os.getenv('KRAKEN_PUBLIC_KEY')
KRAKEN_PRIVATE_KEY = os.getenv('KRAKEN_PRIVATE_KEY')

def request(method: str, path: str, query: Optional[dict] = None, body: dict = {}, environment: str = "https://api.kraken.com") -> http.client.HTTPResponse:
    url = environment + path

    query_str = ""
    if query is not None and len(query):
        query_str = "?" + urllib.parse.urlencode(query)
        url += query_str

    body['nonce'] = get_nonce()

    body_str = json.dumps(body)

    headers = {
        'Content-Type': 'application/json',
        'API-Key': KRAKEN_API_KEY,
        'API-Sign': get_signature(
            private_key=KRAKEN_PRIVATE_KEY, 
            data=query_str + body_str, 
            nonce=body['nonce'], 
            path=path
        ) 
    }

    req = urllib.request.Request(
        method=method,
        url=url,
        headers=headers,
        data=body_str.encode()
    )

    return urllib.request.urlopen(req)

def retrieve_asset_info(symbol: str) -> Tuple[Dict, Dict]:
    response = request(
        method="GET", 
        path="/0/public/Ticker",
        query={'pair': f'{symbol}USD'}
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200:
        return None, json_data['error']

    result = json_data['result']
    values = list(result.values())

    return values[0], None

def retrieve_trades_history() -> Tuple[Dict, Dict]:
    response = request(
        method="POST", 
        path="/0/private/TradesHistory"
    )
    
    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    print(json_data)

    if response.status != 200:
        return None, json_data['error']
        
    result = json_data['result']
    trades = {}

    for trade in result['trades']:
        trades[trade['pair']] = {
            'pair': trade['pair'],
            'time': trade['time'],
            'type': trade['type'],
            'amount': trade['amount'],
            'price': trade['price'],
            'cost': trade['cost'],
            'fee': trade['fee'],
            'margin': trade['margin'],
            'order': trade['order'],
            'pos_open': trade['pos_open'],
            'pos_close': trade['pos_close'],
            'rate': trade['rate'],
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

        if error:
            continue

        current_loss = (asset_info['c'][0] - history['price']) * history['amount'] if history is not None else 0
        total_loss_for_all_assets += current_loss

        portfolio.append({
            'symbol': symbol,
            'amount': float(result[symbol]),
            'price': float(asset_info['c'][0]),
            'value': float(result[symbol]) * float(asset_info['c'][0]),
            'profit_loss': current_loss,
        })

    data = {
        'positions': portfolio,
        'total_profit_loss': total_loss_for_all_assets,
    }

    return data, None