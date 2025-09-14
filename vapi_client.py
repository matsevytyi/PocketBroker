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
            "provider": "openai",
            "model": "gpt-4o-mini",
            "messages": [
                {
                    "role": "system",
                    "content": prompt
                }
            ]
        },
        "firstMessage": first_message,
        "voice": {
            "provider": "vapi",
            "voiceId": "Rohan"
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
    sales_prompt = "You are a friendly sales assistant for ACME Corp. Help customers learn about our products and schedule demos."
    
    try:
        # Show current assistant count
        current_count = count_assistants()
        print(f"Current assistants: {current_count}")
        
        result = create_voice_assistant(sales_prompt, "Hi! Thanks for your interest in ACME Corp. How can I help you today?")
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
