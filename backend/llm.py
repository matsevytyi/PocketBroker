# Import needed libs
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.tools import Tool
# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from typing import Annotated, List, Dict, Any
from dotenv import load_dotenv
import requests
import json
import os
from pydantic import BaseModel, Field
from typing import Literal
import uuid
from openai import OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
import json

# Initialize Gemini model


# SAMPLE DATA
## Example of user data (rag from current portfolio)
current_holdings = """
- Bitcoin (BTC): 0.5 BTC
- Ethereum (ETH): 2.0 ETH  
- Solana (SOL): 50 SOL
- Cardano (ADA): 1000 ADA
"""

## Example of user interest
interest_list = [
    "Buy 25 lllm coin at current market price",
    "Purchase 5 ETH when price drops below $3,200",
    "Sell 25 SOL to take profits at current levels",
    "Buy 500 ADA if price falls to $0.35 or lower",
    "Purchase 10 AVAX as a new position for portfolio diversification"
]

## Load env variables
load_dotenv()

## Initialize models
gemini_llm = ChatGoogleGenerativeAI(model="models/gemini-2.5-flash")# Define Gemini model
client = OpenAI(api_key=os.getenv("XAI_API_KEY"), base_url="https://api.x.ai/v1") # Define OpenAI client for grok search
grok_api_url = "https://api.x.ai/v1/chat/completions"
headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
}
# Define Pydantic schema for Kraken order attributes
class KrakenOrderSchema(BaseModel):
    # ordertype: Literal["limit", "market"] = Field(description="Type of order - limit or market")
    type: Literal["buy", "sell"] = Field(description="Buy or sell order")
    amount: float = Field(description="Number of tokens to buy or sell")
    pair: str = Field(description="Currency pair ID or ALTNAME (e.g., XBTUSD,ticker/currency)")
    symbol: str = Field(description="Symbol of the token to buy or sell (e.g., BTC, ETH, SOL, etc.)")
    quote_currency: str = Field(description="Quote currency of the token to buy or sell (e.g., USD, EUR, etc.)")
    price: str = Field(description="Price for limit orders")

# Define schema for user information
class CurrentHoldingsSchema(BaseModel):
    symbol: str = Field(description="Symbol of the asset (e.g., BTC, ETH, SOL, etc.)")
    holding_amount: float = Field(description="Amount of the asset currently held")
    profit_loss: float = Field(description="Current profit or loss for this asset")
    price: float = Field(description="Current price of the asset")
    value: float = Field(description="Total value of the holding (holding_amount * price)")
    total_profit_loss: float = Field(description="Total profit/loss across all assets in the portfolio")

# Functions to make llm calls

def get_stock_recommendation(current_holdings: str, interest: str) -> str:
    payload = {
    "messages": [
    {
    "role": "user",
    "content": f"""
    # Cryptocurrency Portfolio Analysis and Investment Recommendation

    ## Current Portfolio
    I currently hold the following cryptocurrency positions:

    {current_holdings}

    ## Budget Constraints
    **IMPORTANT**: Only recommend purchases that stay within my available cash budget. My USD holdings represent my available buying power - do not exceed this amount in any recommendation.

    ## Research Request
    Please conduct thorough market research on current cryptocurrency trends, market conditions, and emerging opportunities. Based on this research and my existing portfolio composition, provide a smart diversification recommendation on what i should buy.

    ## Interest
    i am currently interested in the following, please assess the risk and reward of this purchase against any other coin in the market.

    Attempt to follow users interest and budget constraints.

    {interest}

    ## Analysis Requirements
    1. **Market Research**: Analyze current market conditions, trends, and sentiment
    2. **Portfolio Assessment**: Evaluate my current holdings and identify gaps or overexposure
    3. **Diversification Strategy**: Recommend a action that would improve portfolio balance
    4. **Risk Management**: Consider how the recommendation fits my risk profile


    ## Output Format
    Token: [TOKEN_NAME]
    Action: [BUY/SELL/HOLD],
    Price: [PRICE: either a number or a range],
    Quantity: [QUANTITY: either a number or a range],
    Reasoning: [Detailed explanation including market analysis, portfolio fit, risk assessment, and diversification benefits]
    """


    }
    ],
    "search_parameters": {
    "mode": "auto",
    "max_search_results": 10,
    "from_date": "2025-01-01",
    "to_date": "2025-12-31"
    },
    "model": "grok-4"
    }

    response = requests.post(grok_api_url, headers=headers, json=payload)
    print(response.json())
    content = response.json()['choices'][0]['message']['content']
    print(content)
    return content

    #make another call to parse into structured output
    

def parse_for_kraken_order(llm_suggestion:str):
    # Alternative implementation using Gemini and LangChain for structured output


    # Create output parser for structured data
    parser = PydanticOutputParser(pydantic_object=KrakenOrderSchema)

    # Create prompt template with format instructions
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an expert cryptocurrency analyst and portfolio manager. Your task is to parse and structure cryptocurrency trading recommendations from market analysis content.

        The input content follows this format:
        - Token: [TOKEN_NAME] (e.g., BTC (Bitcoin))
        - Action: [BUY/SELL]
        - Reasoning: [Detailed market analysis, portfolio assessment, and risk evaluation]

        IMPORTANT: You must return a SINGLE JSON object (not an array) that matches the KrakenOrderSchema format. If multiple tokens are recommended, choose the PRIMARY recommendation only.
        
        {format_instructions}"""),
        ("user", """Parse the following cryptocurrency trading recommendation and structure it into the required JSON format:

        {content}

        Current Holdings: {current_holdings}

        Extract the PRIMARY token recommendation only. Return a single JSON object (not an array) with the token name, trading action, and detailed reasoning. Ensure all market analysis, portfolio considerations, and risk assessments are preserved in the structured output.""")
    ])

    # Create the chain without parser first to see raw output
    chain_raw = prompt | gemini_llm
    raw_response = {}
    gemini_completion = {}
    try:
        # Execute the chain to get raw output first
        raw_response = chain_raw.invoke({
            "content": llm_suggestion,
            "current_holdings": current_holdings,
            "format_instructions": parser.get_format_instructions()
        })
        
        print("Raw Gemini response:")
        print(raw_response.content)
        print("\n" + "="*50 + "\n")
        
        # Try to parse the raw response
        try:
            # Clean the response content to extract JSON
            response_content = raw_response.content.strip()
            
            # If response starts with ```json, extract the JSON part
            if response_content.startswith("```json"):
                response_content = response_content.split("```json")[1].split("```")[0].strip()
            elif response_content.startswith("```"):
                response_content = response_content.split("```")[1].split("```")[0].strip()
            
            # Parse JSON
            parsed_json = json.loads(response_content)
            
            # If it's a list, take the first item
            if isinstance(parsed_json, list) and len(parsed_json) > 0:
                parsed_json = parsed_json[0]
                print("Warning: Received list, taking first item")
            
            # Validate with Pydantic
            gemini_completion = KrakenOrderSchema.model_validate(parsed_json)
            
            print("Successfully parsed Gemini + LangChain structured output:")
            print(gemini_completion)
            return gemini_completion
            
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing error: {e}")
            print("Raw content that failed to parse:")
            print(repr(response_content))
            
        except Exception as e:
            print(f"Pydantic validation error: {e}")
            print("Parsed JSON that failed validation:")
            print(parsed_json)

            
    except Exception as e:
        print(f"Chain execution error: {e}")

def attempt_order_with_intent(intent: str, portfolio: str):
    stock_recommendation = get_stock_recommendation(current_holdings=portfolio, interest=interest_list[1])
    parsed_results = parse_for_kraken_order(stock_recommendation)
    return parsed_results
## Test the functions

# attempt_order_with_intent(intent=interest_list[1], current_holdings=current_holdings)
