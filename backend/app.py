from flask import Flask, jsonify
from dotenv import load_dotenv
from service import request, retrieve_asset_info, retrieve_portfolio
import json

load_dotenv()

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run(debug=True, port=8080)