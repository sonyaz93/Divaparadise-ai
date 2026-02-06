import sys
import os
import argparse

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from text_client import TextClient

def main():
    print("[INFO] Initializing Thinking Lab 🧠...")
    
    # Default Riddle
    prompt = "I speak without a mouth and hear without ears. I have no body, but I come alive with wind. What am I?"
    budget = 1024 # Default Thinking Budget
    
    if len(sys.argv) > 1:
        prompt = sys.argv[1]
    
    # Using a model that supports thinking (Gemini 2.5 or 3 Flash)
    # Note: text_client defaults to gemini-3-flash-preview which supports it.
    client = TextClient(model_name="gemini-2.0-flash-exp") 
    
    print(f"\n--- PROMPT ---\n{prompt}")
    print(f"\n--- THINKING ({budget} tokens) ---")
    print("...")
    
    result = client.generate_text(prompt, thinking_budget=budget)
    
    if result:
        print("\n--- RESULT ---")
        print(result)
    else:
        print("[FAIL] Thinking failed.")

if __name__ == "__main__":
    main()
