import json
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from service import retrieve_asset_info, retrieve_portfolio, execute_buy_order, retrieve_asset_pair_name, execute_sell_order
from llm import get_stock_recommendation, parse_for_kraken_order,attempt_order_with_intent

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

    data = response.values()

    return jsonify({'data': data, 'error': False}), 200

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

    pair = request_body['pair']
    amount = request_body['amount']
    order_type = request_body['ordertype']
    price = request_body.get('price', None)

    response, error = execute_buy_order(
        pair=pair,
        amount=amount,
        order_type=order_type,
        price=price
    )

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/sell", methods=["POST"])
def sell():
    request_body = request.get_json()

    pair = request_body['pair']
    amount = request_body['amount']
    order_type = request_body['ordertype']
    price = request_body.get('price', None)

    response, error = execute_sell_order(
        pair=pair,
        amount=amount,
        order_type=order_type,
        price=price
    )

    if error:
        return jsonify({'details': error, 'error': True}), 500

    return jsonify({'data': response, 'error': False}), 200

@app.route("/api/v1/orders", methods=["GET"])
def orders():
    pass



@app.route("/api/v1/attempt_order", methods=["POST"])
def attempt_order():
    request_body = request.get_json()

    # Validate request body contains intent
    # Intent is what the user wants to do with the stock "I want to buy BTC, I want to sell 2 XRP token, etc."
    if not request_body or 'intent' not in request_body:
        return jsonify({'details': 'Missing intent in request body', 'error': True}), 400
    intent = request_body['intent']
    
    # Get current portfolio
    response, error = retrieve_portfolio()
    if error:
        return jsonify({'details': error, 'error': True}), 500

    print(response)

   
    # make order details with helper function
    order_details = attempt_order_with_intent(str(intent), json.dumps(response))
    print("order details")
    print(order_details)

    # Handle potential error from LLM function
    if not order_details:
        return jsonify({'details': 'Failed to parse order intent', 'error': True}), 500

    print(order_details)
    
    # get sell or buy intent from "type"
    type = order_details.type
    if type == "buy":
        order_response = execute_buy_order(
            pair=order_details.pair,
            amount=order_details.amount,
            order_type="market",)
    else:
        order_response = execute_sell_order(
            pair=order_details.pair,
            amount=order_details.amount,
            order_type="market",)
    

    response_data, error = order_response
    
    if error:
        return jsonify({'details': error, 'error': True}), 500
    else:
        return jsonify({'data': response_data, 'error': False}), 200



if __name__ == '__main__':
    app.run(debug=True, port=9080)