# Import needed libs
# from langchain_community.tools import DuckDuckGoSearchRun
# from langchain_community.document_loaders import WebBaseLoader
# from langchain.tools import Tool
# from langchain.agents import AgentExecutor, create_tool_calling_agent
# from langchain.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import requests
import os
import json

# Initialize Gemini model

from typing import Dict, Optional
from dotenv import load_dotenv
import requests
import json

## Load env variables
load_dotenv()

## Initialize models
grok_api_url = "https://api.x.ai/v1/chat/completions"

def get_payload(portfolio: Dict, interest: Optional[str] = None):
    return {
        "messages": [
            {
                "role": "user",
                "content": f"""
                # Cryptocurrency Portfolio Analysis and Investment Recommendation

                ## Current Portfolio
                I currently hold the following cryptocurrency positions:

                {portfolio}


                ## Research Request
                Please conduct thorough market research on current cryptocurrency trends, market conditions, and emerging opportunities. Based on this research and my existing portfolio composition, provide a smart diversification recommendation on what i should buy.

                ## Interest
                {interest}

                ## Analysis Requirements
                1. **Market Research**: Analyze current market conditions, trends, and sentiment
                2. **Portfolio Assessment**: Evaluate my current holdings and identify gaps or overexposure
                3. **Diversification Strategy**: Recommend a action that would improve portfolio balance
                4. **Risk Management**: Consider how the recommendation fits my risk profile

                ## Output Format
                Token: [TOKEN_NAME]
                Action: [BUY/SELL/HOLD],
                Price: [PRICE],
                Quantity: [QUANTITY],
                Reasoning: [Detailed explanation including market analysis, portfolio fit, risk assessment, and diversification benefits]
                """
            }
            ],
            "search_parameters": {
                "mode": "auto",
                "max_search_results": 5,
                "from_date": "2025-01-01",
                "to_date": "2025-12-31"
            },
            "model": "grok-3"
        }

def send_grok_request(payload: Dict):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.getenv('XAI_API_KEY')}"
    }

    response = requests.post(grok_api_url, headers=headers, json=get_payload(payload))
    return response.json()
