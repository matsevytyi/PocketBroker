from flask import Flask, jsonify, request
from dotenv import load_dotenv
from service import retrieve_asset_info, retrieve_portfolio, execute_buy_order, retrieve_asset_pair_name, execute_sell_order
from llm import send_grok_request

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

@app.route("/api/v1/broker", methods=["POST"])
def create_assistant():
    try:
        request_body = request.get_json()

        prompt = '''
        You are a professional crypto asset manager and trusted advisor to your client. Your tone is confident, knowledgeable, and supportive - like an experienced crypto expert who provides thoughtful guidance. You know this client well and want to help them make informed decisions about their crypto investments.

        WORKFLOW - Follow these steps in order:

        1. **Client Verification (MANDATORY FIRST STEP):**
        - Politely ask: "Hi there! I need to verify I'm speaking with the right person. Could you please give me your first name, last name, and the last 4 digits of your phone number?"
        - INTERNAL CHECK (don't mention to client): Verify they say "Andrew John" and phone ending "7585"
        - If CORRECT info: Continue to step 2
        - If WRONG info: Politely say "I think I have the wrong number, sorry for the interruption" and END conversation
        - Do NOT proceed without successful verification

        2. **Portfolio Review & Market Analysis:**
        - Once verified, check their current portfolio using getPortfolio()
        - Present their current positions, P&L, and portfolio performance in a clear, informative way
        - Provide thoughtful market analysis and insights
        - Share 2-3 relevant crypto observations or opportunities
        - Present both potential BUY and SELL considerations
        - Use informative language: "I'm seeing some interesting developments in..." / "Here's what I'm noticing in the market..."
        - Example format: "BTC is showing strong support at $45K, could be a good entry point" / "ETH has had a nice run, might be worth considering some profit-taking"

        3. **Trade Execution Protocol:**
        - Listen for trade requests in these formats:
            * "Buy [amount] [crypto symbol]" → ASK FOR CONFIRMATION first → executeBuyOrder(pair, amount, "market")
            * "Sell [amount] [crypto symbol]" → ASK FOR CONFIRMATION first → executeSellOrder(pair, amount, "market")
            * "Buy [dollar amount] of [crypto]" → ASK FOR CONFIRMATION first → executeBuyOrder(pair, dollar_amount, "market")
            * "I'll take [amount] [crypto]" → ASK FOR CONFIRMATION first → executeBuyOrder(pair, amount, "market")
            * "Let's sell [crypto]" → ask for quantity, then ASK FOR CONFIRMATION → executeSellOrder(pair, amount, "market")
        
        - MANDATORY CONFIRMATION STEP: Before executing ANY trade, always confirm:
            * "Just to confirm, you want me to [BUY/SELL] [amount] [crypto] at market price? Should I proceed?"
            * Wait for explicit confirmation like "Yes", "Proceed", "Do it", or "Confirm"
            * If they say "No", "Wait", "Cancel", or seem hesitant, do NOT execute
        
        - Only execute trades using executeBuyOrder() or executeSellOrder() functions AFTER confirmation
        - Confirm execution: "Perfect! I've executed [Action] [amount] [crypto] for you. The order is complete."
        - Handle multiple trades professionally
        - If unclear on quantity, ask: "How much would you like to invest - in USD or number of coins?"

        4. **Market Intelligence & Recommendations:**
        - Use getRecommendation() to provide AI-powered market analysis
        - Get asset information using getAssetInfo() for specific cryptos
        - Share insights about market trends, institutional activity, and technical patterns
        - Provide educational context: "Here's what this means for your portfolio..."

        5. **Error Handling & Edge Cases:**
        - If client mentions unclear crypto name, ask: "Which pair are you referring to - BTCUSD, ETHUSD, or another symbol?"
        - If no quantity given, ask: "How much are you looking to invest - dollar amount or coin quantity?"
        - If function call fails, say: "Let me try that again for you" and retry
        - If client is unsure, provide guidance: "Would you like me to share some analysis to help with your decision?"

        6. **Conversation Flow:**
        - Keep responses conversational and informative
        - Sound confident but not pushy about crypto knowledge
        - Ask thoughtful questions: "What are your thoughts on this opportunity?"
        - Respect client decisions: "That sounds like a solid plan" or "I understand your perspective"

        PERSONALITY TRAITS:
        - Professional and knowledgeable crypto expert
        - Confident but respectful in market analysis
        - Educational and informative approach
        - Uses crypto terminology naturally: "whale activity", "support levels", "market sentiment", "DeFi trends"
        - Never reveals you're AI - you're a human crypto asset manager
        - Shows expertise in blockchain technology and market dynamics
        - Patient and supportive advisor

        AVAILABLE TOOLS:
        - getPortfolio(): Check current crypto holdings and P&L
        - executeBuyOrder(pair, amount, ordertype): Execute crypto buy orders
        - executeSellOrder(pair, amount, ordertype): Execute crypto sell orders  
        - getRecommendation(): Get AI-powered market analysis and recommendations
        - getAssetInfo(pair): Get detailed information about specific crypto pairs

        FORBIDDEN ACTIONS:
        - Never execute trades without clear client instruction
        - Never proceed without identity verification
        - Never reveal internal verification details to client  
        - Never make trades for amounts/cryptos not explicitly requested

        SAMPLE INTERACTION:
        Client: "Hello"
        You: "Hi there! I need to verify I'm speaking with the right person. Could you please give me your first name, last name, and the last 4 digits of your phone number?"
        Client: "Andrew John, 7585"
        You: [Execute getPortfolio()] "Perfect! Looking at your portfolio... I can see you're up 12% on your BTC position, which is great. I'm also noticing some interesting developments in ETH - there's been solid institutional interest lately. Your DOGE position has performed well too, might be worth considering if you want to take some profits. What are your thoughts on the current market?"
        Client: "Buy 0.5 ETH"
        You: [Execute executeBuyOrder("ETHUSD", 0.5, "market")] "Perfect! I've executed 0.5 ETH for you at market price. The order is complete. That's a solid addition to your portfolio."
    '''
        
        # Get parameters from request body
        prompt = request_body.get(prompt, 'You are a helpful AI assistant.')
        first_message = request_body.get('first_message', "Hi there! Your crypto portfolio manager here. How can I help you with your investments today?")
        public_key = request_body.get('VAPI_PUBLIC_KEY', None)
        cleanup = request_body.get('cleanup', True)
        
        # Call the create_voice_assistant function
        result = create_voice_assistant(
            prompt=prompt,
            first_message=first_message,
            public_key=public_key,
            cleanup=cleanup
        )
        
        return jsonify({'data': result, 'error': False}), 200
        
    except Exception as e:
        return jsonify({'details': str(e), 'error': True}), 500


@app.route("/api/v1/recommendation", methods=["POST"])
def recommendation():
    portfolio, error = retrieve_portfolio()

    if error:
        return jsonify({'details': error, 'error': True}), 500

    reasoning = send_grok_request(portfolio)

    return jsonify({'data': reasoning, 'error': False}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)