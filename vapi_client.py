"""
Simple VAPI Web Client for Voice AI

This module provides a simple implementation for creating web-based voice AI
assistants using VAPI's API.
"""

import os
import requests
import time
from typing import List, Dict
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def list_assistants() -> List[Dict]:
    """List all existing assistants"""
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        raise Exception("VAPI_API_KEY not found in environment variables")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(
            "http://api.vapi.ai/assistant",
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Failed to list assistants: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        if "Failed to resolve" in str(e) or "getaddrinfo failed" in str(e):
            raise Exception("Network connectivity issue - check your internet connection")
        raise Exception(f"Error listing assistants: {str(e)}")

def delete_assistant(assistant_id: str) -> bool:
    """Delete a specific assistant"""
    api_key = os.getenv("VAPI_API_KEY")
    if not api_key:
        raise Exception("VAPI_API_KEY not found in environment variables")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.delete(
            f"http://api.vapi.ai/assistant/{assistant_id}",
            headers=headers,
            timeout=10
        )
        
        return response.status_code in [200, 204]
        
    except requests.exceptions.RequestException as e:
        if "Failed to resolve" in str(e) or "getaddrinfo failed" in str(e):
            raise Exception("Network connectivity issue - check your internet connection")
        raise Exception(f"Error deleting assistant: {str(e)}")

def cleanup_old_assistants(keep_count: int = 5) -> int:
    """Delete old assistants, keeping only the most recent ones"""
    try:
        assistants = list_assistants()
        
        if len(assistants) <= keep_count:
            print(f"Found {len(assistants)} assistants, no cleanup needed")
            return 0
        
        # Sort by creation date (assuming they have createdAt field)
        assistants.sort(key=lambda x: x.get('createdAt', ''), reverse=True)
        
        # Delete older assistants
        deleted_count = 0
        for assistant in assistants[keep_count:]:
            try:
                if delete_assistant(assistant['id']):
                    deleted_count += 1
                    print(f"Deleted assistant: {assistant['id']}")
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                print(f"Failed to delete {assistant['id']}: {e}")
        
        return deleted_count
        
    except Exception as e:
        print(f"Cleanup failed: {e}")
        return 0

def create_voice_assistant(
    prompt: str,
    first_message: str = "Hello! How can I help you today?",
    public_key: str = None,
    cleanup: bool = True
) -> dict:
    """
    Create a voice assistant and generate an HTML file to interact with it
    
    Args:
        prompt: The system prompt for the assistant
        first_message: The first message the assistant will say
        public_key: VAPI public key (optional, will use API key if not provided)
        
    Returns:
        Path to the generated HTML file
    """
    api_key = os.getenv('VAPI_API_KEY')
    if not api_key:
        raise Exception("VAPI_API_KEY not found in environment variables")
    
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    
    # Cleanup old assistants if requested
    if cleanup:
        try:
            deleted = cleanup_all_assistants()
            if deleted > 0:
                print(f"Cleaned up {deleted} old assistants")
        except Exception as e:
            print(f"Cleanup warning: {e}")
    
    # Create assistant
    assistant_body = {
        "name": "Web Voice Assistant",
        "model": {
            "provider": "google",
            "model": "gemini-2.5-flash",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                }
            ],
            "tools": [
            {
                "type": "apiRequest",
                "function": { "name": "api_request_tool" },
                "name": "getPortfolio",
                "url": "https://pocketbroker.vercel.app/api/v1/portfolio",
                "method": "GET"
            },
            {
                "type": "apiRequest",
                "function": { "name": "api_request_tool" },
                "name": "getAssetInfo",
                "url": "https://pocketbroker.vercel.app/api/v1/assets/{{pair}}",
                "method": "GET",
                "body": {
                    "type": "object",
                    "properties": {
                    "pair": {
                        "description": "Trading pair ALTNAME, e.g., ETHUSDT or BTCUSD",
                        "type": "string"
                    }
                    },
                    "required": ["pair"]
                }
            },
            {
                "type": "apiRequest",
                "function": { "name": "api_request_tool" },
                "name": "getRecommendation",
                "url": "https://pocketbroker.vercel.app/api/v1/recommendation",
                "method": "POST",
                "body": {
                    "type": "object",
                    "properties": {
                    "userId": { "type": "string", "description": "Internal user id" },
                    "strategy": {
                        "type": "string",
                        "enum": ["conservative","balanced","aggressive"],
                        "description": "Optional preset"
                    },
                    "preferences": {
                        "type": "object",
                        "description": "Optional user prefs",
                        "properties": {
                        "risk": { "type": "string", "enum": ["low","medium","high"] },
                        "time_horizon": { "type": "string" },
                        "preferred_quote": { "type": "string" }
                        }
                    },
                    "use_fresh": {
                        "type": "boolean",
                        "description": "Force backend to refetch portfolio from broker"
                    },
                    "snapshot": {
                        "type": "object",
                        "description": "Optional portfolio snapshot hint",
                        "properties": {
                        "positions": {
                            "type": "array",
                            "items": {
                            "type": "object",
                            "properties": {
                                "symbol": { "type": "string" },
                                "quote":  { "type": "string" },
                                "quantity": { "type": "number" },
                                "cost_basis": { "type": "number" }
                            },
                            "required": ["symbol","quote","quantity"]
                            }
                        },
                        "asof": { "type": "string", "description": "ISO timestamp" },
                        "hash": { "type": "string", "description": "Deterministic snapshot hash" },
                        "ttl_seconds": { "type": "number", "description": "Freshness window" }
                        }
                    }
                    },
                    "required": ["userId"]
                }
            },
            {
                "type": "apiRequest",
                "function": { "name": "api_request_tool" },
                "name": "executeBuyOrder",
                "url": "https://pocketbroker.vercel.app/api/v1/buy",
                "method": "POST",
                "body": {
                    "type": "object",
                    "properties": {
                        "pair": {
                            "type": "string",
                            "description": "Trading pair (e.g., ETHUSDT, BTCUSD)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to buy"
                        },
                        "ordertype": {
                            "type": "string",
                            "description": "Order type (e.g., market, limit)"
                        },
                        "price": {
                            "type": "number",
                            "description": "Price for limit orders (optional)"
                        }
                    },
                    "required": ["pair", "amount", "ordertype"]
                }
            },
            {
                "type": "apiRequest",
                "function": { "name": "api_request_tool" },
                "name": "executeSellOrder",
                "url": "https://pocketbroker.vercel.app/api/v1/sell",
                "method": "POST",
                "body": {
                    "type": "object",
                    "properties": {
                        "pair": {
                            "type": "string",
                            "description": "Trading pair (e.g., ETHUSDT, BTCUSD)"
                        },
                        "amount": {
                            "type": "number",
                            "description": "Amount to sell"
                        },
                        "ordertype": {
                            "type": "string",
                            "description": "Order type (e.g., market, limit)"
                        },
                        "price": {
                            "type": "number",
                            "description": "Price for limit orders (optional)"
                        }
                    },
                    "required": ["pair", "amount", "ordertype"]
                }
            }
        ],
        },
        "firstMessage": first_message,
        "voice": {
            "provider": "vapi",
            "voiceId": "Rohan",
            # Add customizations here:
            "speed": 1.6   # >1.0 = faster, <1.0 = slower (default = 1.0)
        }
    }
    
    try:
        response = requests.post(
            "https://api.vapi.ai/assistant",
            headers=headers,
            json=assistant_body,
            timeout=10
        )
        
        if response.status_code in [200, 201]:
            assistant = response.json()
            assistant_id = assistant["id"]
            
            # Return assistant ID and frontend URL
            frontend_url = f"http://matsevytyi.github.io/PocketBroker/?assistant_id={assistant_id}"
            
            return {
                "assistant_id": assistant_id,
                "frontend_url": frontend_url,
                "message": f"Assistant created! Access at: {frontend_url}"
            }
        else:
            raise Exception(f"Failed to create assistant: {response.status_code} - {response.text}")
            
    except requests.exceptions.RequestException as e:
        if "Failed to resolve" in str(e) or "getaddrinfo failed" in str(e):
            raise Exception("Network connectivity issue - check your internet connection")
        raise Exception(f"Error creating voice assistant: {str(e)}")
    except Exception as e:
        raise Exception(f"Error creating voice assistant: {str(e)}")


# Utility functions for assistant management
def count_assistants() -> int:
    """Get count of existing assistants"""
    try:
        assistants = list_assistants()
        return len(assistants)
    except Exception:
        return 0

def cleanup_all_assistants() -> int:
    """Delete all assistants"""
    try:
        assistants = list_assistants()
        deleted_count = 0
        for assistant in assistants:
            if delete_assistant(assistant['id']):
                deleted_count += 1
                print(f"Deleted assistant: {assistant['id']}")
            time.sleep(0.5)  # Rate limiting
        return deleted_count
    except Exception as e:
        print(f"Cleanup all failed: {e}")
        return 0


# Example usage
if __name__ == "__main__":
    # Example: Create a crypto asset manager assistant
    sales_prompt = '''
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

        MINIMUM TRADING AMOUNTS (Important - Always Check Before Trading):
        - Solana (SOL): Minimum 0.02 SOL
        - Bitcoin (BTC): Minimum 0.00005 BTC  
        - Ethereum (ETH): Minimum 0.002 ETH
        - Ripple (XRP): Minimum 1.65 XRP
        
        TRADING VALIDATION:
        - Always verify the requested amount meets the minimum requirements before confirmation
        - If amount is below minimum, inform client: "The minimum for [crypto] is [amount]. Would you like to adjust your order?"
        - Suggest rounding up to minimum if client requests below threshold

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
    
    try:
        # Show current assistant count
        current_count = count_assistants()
        print(f"Current assistants: {current_count}")
        
        result = create_voice_assistant(sales_prompt, "Hi there! Your crypto portfolio manager here. How can I help you with your investments today?", cleanup=False)
        print(f"Assistant ID: {result['assistant_id']}")
        print(f"Frontend URL: {result['frontend_url']}")
        print(result['message'])
    except Exception as e:
        print(f"Error: {e}")
        
        # If network error, suggest checking connection
        if "Network connectivity" in str(e):
            print("\nTroubleshooting tips:")
            print("1. Check your internet connection")
            print("2. Try again in a few moments")
            print("3. Verify VAPI service status")
