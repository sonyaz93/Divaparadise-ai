import sys
import os
import logging
import json

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.batch_client import BatchClient
from api.batch_types import BatchRequestInput, GenerateContentRequest

# Setup Logging
logger = logging.getLogger("BatchLab")
logging.basicConfig(level=logging.INFO)

def main():
    print("📦 Gemini Batch Processing Lab 📦")
    print("---------------------------------")
    
    client = BatchClient()
    model = "models/gemini-1.5-flash" # Use full resource name for batches usually
    
    # 1. Create a Batch of 5 requests
    print("\nPreparing Batch Requests...")
    prompts = [
        "Explain quantum entanglement.",
        "Write a haiku about code.",
        "What is the capital of Paris?",
        "List 3 distinct colors.",
        "Translate 'Hello' to Spanish."
    ]
    
    requests = []
    for p in prompts:
        req = GenerateContentRequest(
            model=model,
            contents=[{"parse": {"text": p}}] # Note: Content structure dict
            # Actually, standard structure is {"role": "user", "parts": [{"text": ...}]}
        )
        # Fixing structure for compatibility
        req.contents = [{"role": "user", "parts": [{"text": p}]}]
        requests.append(req)
        
    input_data = BatchRequestInput(requests=requests)
    
    try:
        print(f"Submitting Batch to {model}...")
        batch = client.create_batch(
            model=model, 
            input_data=input_data, 
            display_name="lab_test_batch"
        )
        batch_name = batch.get("name")
        print(f"✅ Batch Created: {batch_name}")
        print(f"Initial State: {batch.get('state')}")
        
        # 2. Monitor (Optional - user can skip with Ctrl+C)
        print("\nMonitoring (Press Ctrl+C to stop)...")
        final_batch = client.monitor_batch(batch_name, poll_interval=5)
        
        print("\n🏁 Final Status:")
        print(json.dumps(final_batch, indent=2))
        
        # 3. Retrieve Results (if succeeded)
        output_uri = final_batch.get("output", {}).get("responsesFile")
        if output_uri:
            print(f"\nResults available at: {output_uri}")
            print("(Download logic would involve GETing this URI with auth)")
            
    except Exception as e:
        logger.error(f"Batch Failed: {e}")

if __name__ == "__main__":
    main()
