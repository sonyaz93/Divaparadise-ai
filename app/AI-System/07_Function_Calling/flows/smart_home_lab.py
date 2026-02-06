import sys
import os

# Add Path to 05 module to reuse TextClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../05_Text_Generation/api")))
from text_client import TextClient

# Import Tools
from tools_library import ALL_TOOLS

def main():
    print("[INFO] Initializing Smart Home Lab 🏠...")
    
    # Initialize Client with Access to ALL Tools
    client = TextClient()
    
    # Scenario 1: Parallel Function Calling
    # The model should call BOTH power_disco_ball and start_music in a single turn.
    prompt_party = "Turn this place into a party! Start the disco ball and play some loud, energetic music."
    
    print(f"\n--- SCENARIO 1: PARALLEL EXECUTION ---\nUser: {prompt_party}")
    
    response_party = client.generate_text(
        prompt_party,
        tools=ALL_TOOLS,
        thinking_budget=1024 # Reasoning helps decide WHICH tools to use
    )
    
    print(f"\n[AI RESPONSE]:\n{response_party}")

    # Scenario 2: Compositional / Logic
    # The model works with light settings.
    prompt_chill = "Set the lights to 50% brightness and make it warm for a movie night."
    
    print(f"\n--- SCENARIO 2: LIGHT CONTROL ---\nUser: {prompt_chill}")
    
    response_chill = client.generate_text(
        prompt_chill,
        tools=ALL_TOOLS
    )
    print(f"\n[AI RESPONSE]:\n{response_chill}")

if __name__ == "__main__":
    main()
