import sys
import os
import json

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from text_client import TextClient

def main():
    print("[INFO] Initializing Structured Lab 🧱...")
    
    client = TextClient()
    
    # 1. Define the Schema (Standard JSON Schema format or simple Dict mapping)
    # We want to extract an RPG Character Profile.
    character_schema = {
        "type": "object",
        "properties": {
            "name": {"type": "string", "description": "Character Name"},
            "class": {"type": "string", "enum": ["Warrior", "Mage", "Rogue", "Hacker"]},
            "stats": {
                "type": "object",
                "properties": {
                    "strength": {"type": "integer"},
                    "intelligence": {"type": "integer"},
                    "dexterity": {"type": "integer"}
                }
            },
            "inventory": {
                "type": "array",
                "items": {"type": "string"}
            },
            "backstory": {"type": "string", "description": "Short bio"}
        },
        "required": ["name", "class", "stats", "inventory", "backstory"]
    }
    
    prompt = "Create a legendary Cyberpunk Hacker named 'Zero-Cool'. He is elite at breaking encryption. Give him cool gear."
    if len(sys.argv) > 1:
        prompt = sys.argv[1]

    print(f"\n--- PROMPT ---\n{prompt}")
    print("\n--- GENERATING STRUCT DATA ---")
    
    # Generate with Schema
    json_result = client.generate_text(
        prompt, 
        output_schema=character_schema,
        temperature=0.7
    )
    
    if json_result:
        print("\n--- RAW JSON RESULT ---")
        print(json_result)
        
        try:
            data = json.loads(json_result)
            print(f"\n[SUCCESS] Parsed Character: {data.get('name')} ({data.get('class')})")
            print(f"Stats: {data.get('stats')}")
            print(f"Inventory: {data.get('inventory')}")
        except:
            print("[FAIL] Could not parse JSON.")
    else:
        print("[FAIL] Generation failed.")

if __name__ == "__main__":
    main()
