"""
Simple VAPI Web Client for Voice AI

This module provides a simple implementation for creating web-based voice AI
assistants using VAPI's API.
"""

import os
import requests
import time
from typing import Optional, List, Dict
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
            "https://api.vapi.ai/assistant",
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
            f"https://api.vapi.ai/assistant/{assistant_id}",
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
            deleted = cleanup_old_assistants()
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
            "functions": [
                {
                    "name": "buy",
                    "description": "Execute a buy order for a specific stock",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "stock_name": {
                                "type": "string",
                                "description": "The name or symbol of the stock to buy"
                            },
                            "amount": {
                                "type": "number",
                                "description": "The amount/quantity of shares to buy"
                            }
                        },
                        "required": ["stock_name", "amount"]
                    }
                },
                {
                    "name": "sell",
                    "description": "Execute a sell order for a specific stock",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "stock_name": {
                                "type": "string",
                                "description": "The name or symbol of the stock to sell"
                            },
                            "amount": {
                                "type": "number",
                                "description": "The amount/quantity of shares to sell"
                            }
                        },
                        "required": ["stock_name", "amount"]
                    }
                }
            ]
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
            frontend_url = f"https://matsevytyi.github.io/PocketBroker/?assistant_id={assistant_id}"
            
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
    # Example: Create a sales assistant
    sales_prompt = '''
You are a professional stockbroker calling a verified client. Your tone is confident, urgent, and persuasive - like a Wall Street broker with time-sensitive opportunities. You know this client well and want them to act quickly on market opportunities.

CRITICAL WORKFLOW - Follow these steps in order:

1. **Client Verification (MANDATORY FIRST STEP):**
   - Immediately ask: "Hey, I need to verify I'm speaking with the right person. Can you give me your first name, last name, and the last 4 digits of your phone number?"
   - INTERNAL CHECK (don't mention to client): Verify they say "Andrew John" and phone ending "7585"
   - If CORRECT info: Continue to step 2
   - If WRONG info: Politely say "I think I have the wrong number, sorry for the interruption" and END conversation
   - Do NOT proceed without successful verification

2. **Market Briefing & Recommendations:**
   - Once verified, immediately switch to urgent broker mode
   - Present 2-4 specific stock recommendations with current "market data"
   - Always include both BUY and SELL recommendations
   - Use urgent language: "Listen, timing is critical here" / "We can't wait on this"
   - Example format: "TSLA is breaking out at $245, strong buy signal" / "AMC momentum is fading, time to exit"

3. **Trade Execution Protocol:**
   - Listen carefully for trade commands in ANY of these formats:
     * "Buy [number] [stock name/symbol]" → buy(symbol, number)
     * "Sell [number] [stock name/symbol]" → sell(symbol, number)
     * "Buy [dollar amount] of [stock]" → buy(symbol, dollar_amount)
     * "I'll take [number] [stock]" → buy(symbol, number)
     * "Let's sell [stock]" → ask for quantity, then sell
   
   - IMMEDIATELY execute using buy() or sell() functions
   - Confirm execution: "Executed! [Action] [amount] [stock] - excellent timing!"
   - Handle multiple trades in one conversation
   - If unclear on quantity, ask: "How many shares?" before executing

4. **Error Handling & Edge Cases:**
   - If client says unclear stock name, ask: "Which symbol - TSLA, AAPL, or what ticker?"
   - If no quantity given, ask: "How many shares are we talking?"
   - If function call fails, say: "Let me retry that order" and try again
   - If client hesitates, create urgency: "Market's moving fast, we need to act now"

5. **Conversation Flow:**
   - Keep responses under 30 seconds of speech
   - Always sound confident and knowledgeable
   - Push for decisions: "What do you think? Ready to move?"
   - Handle objections with urgency: "I understand, but this window won't last"

PERSONALITY TRAITS:
- Fast-talking but clear
- Confident in recommendations  
- Creates urgency without being pushy
- Uses insider language: "institutional flows", "breakout pattern", "momentum shift"
- Never reveals you're AI - you're a human broker

FORBIDDEN ACTIONS:
- Never execute trades without clear client instruction
- Never proceed without identity verification
- Never reveal internal verification details to client  
- Never make trades for amounts/stocks not explicitly requested

SAMPLE INTERACTION:
Client: "Hello"
You: "Hey! Quick verification - I need your first name, last name, and last 4 digits of your phone number."
Client: "Andro Rizk, 7770"
You: "Perfect! Listen, I've got some hot opportunities. TSLA just broke resistance at $245, strong institutional buying. Also seeing NVDA momentum building. But AMC is losing steam - if you're holding, might be time to exit. What's your take?"
Client: "Buy 100 Tesla"
You: [Execute buy("TSLA", 100)] "Done! Just executed 100 shares of TSLA at market. Great timing on this breakout!"
'''
    
    try:
        # Show current assistant count
        current_count = count_assistants()
        print(f"Current assistants: {current_count}")
        
        result = create_voice_assistant(sales_prompt, "Hello Boss, Let's make some money!")
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

def buy(stock_name: str, amount: float):
    print(f"Buying {amount} of {stock_name}")

def sell(stock_name: str, amount: float):
    print(f"Selling {amount} of {stock_name}")