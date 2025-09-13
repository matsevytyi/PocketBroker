from flask import Flask, jsonify, request
from dotenv import load_dotenv
from service import retrieve_asset_info, retrieve_portfolio, execute_buy_order, retrieve_asset_pair_name, execute_sell_order

load_dotenv()

app = Flask(__name__)

@app.route("/api/v1/pairs", methods=["POST"])
def get_pair_name():
    request_body = request.get_json()

    symbol1 = request_body['symbol1']
    symbol2 = request_body['symbol2']

    response, error = retrieve_asset_pair_name(symbol1, symbol2)

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/asset/<ticker>", methods=["GET"])
def get_asset(ticker: str):
    response, error = retrieve_asset_info(ticker)

    if error:
        return jsonify({'error': True, 'details': error}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/portfolio", methods=["GET"])
def get_portfolio():
    response, error = retrieve_portfolio()

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/buy", methods=["POST"])
def buy():
    request_body = request.get_json()

    symbol = request_body['symbol']
    quote_currency = request_body['quote_currency']
    amount = request_body['amount']

    response, error = execute_buy_order(
        symbol=symbol,
        amount=amount,
        quote_currency=quote_currency
    )

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/sell", methods=["POST"])
def sell():
    request_body = request.get_json()

    symbol = request_body['symbol']
    quote_currency = request_body['quote_currency']
    amount = request_body['amount']

    response, error = execute_sell_order(
        symbol=symbol,
        amount=amount,
        quote_currency=quote_currency
    )

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/orders", methods=["GET"])
def orders():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=8080)