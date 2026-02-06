import sys
import os
import time

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from text_client import TextClient

# --- Define Tools ---
def get_current_weather(location: str):
    """
    Get the current weather in a given location.
    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    print(f"\n[TOOL] 🌍 Checking weather for: {location}...")
    # Mock Data
    if "london" in location.lower():
        return "Rainy, 12°C"
    elif "tokyo" in location.lower():
        return "Sunny, 22°C"
    elif "california" in location.lower():
        return "Sunny, 25°C"
    else:
        return "Cloudy, 18°C"

# --- Main ---
def main():
    print("[INFO] Initializing Agent Lab 🤖...")
    print("Agent: Weather Bot (Powered by Gemini Thinking + Tools)")
    
    # Initialize with a Thinking Model
    client = TextClient(model_name="gemini-2.0-flash-exp")
    
    # Define Tools List
    tools = [get_current_weather]
    
    # Start Chat with Tools (Enables Automatic Function Calling)
    chat = client.start_chat(tools=tools)
    
    # User Query
    user_query = "Should I wear a raincoat in London today? And how about Tokyo?"
    if len(sys.argv) > 1:
        user_query = sys.argv[1]

    print(f"\nUser: {user_query}")
    print("\n--- AGENT WORKING ---")
    
    # Send message (SDK handles the loop: Model -> Tool Call -> Execute -> Model -> Answer)
    # We might not see the intermediate thoughts/calls printed by the SDK directly unless we configure logging,
    # but the tool function print statement "[TOOL]" will show us it's working.
    response = chat.send_message(user_query)
    
    print("\n--- AGENT RESPONSE ---")
    print(f"Bot: {response.text}")

if __name__ == "__main__":
    main()
