from flask import Flask, jsonify
from dotenv import load_dotenv
from service import request
import json

load_dotenv()

app = Flask(__name__)

@app.route("/api/v1/asset/<ticker>", methods=["GET"])
def get_asset(ticker: str):
    response = request(
        method="GET", 
        path="/0/public/Ticker",
        query={'pair': f'{ticker}CAD'}
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200:
        return jsonify({'error': True, 'details': json_data['error']}), response.status

    result = json_data['result']
    values = list(result.values())

    return jsonify({'data': values[0], 'error': False}), 200

@app.route("/api/v1/portfolio", methods=["GET"])
def get_portfolio():
    response = request(
        method="POST", 
        path="/0/private/Balance"
    )

    response_data = response.read().decode('utf-8')

    json_data = json.loads(response_data)

    if response.status != 200:
        return jsonify({'error': True, 'details': json_data['error']}), response.status

    result = json_data['result']

    return jsonify({'data': result, 'error': False}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)