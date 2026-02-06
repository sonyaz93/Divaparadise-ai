import sys
import os
import logging
import json

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.interactions_client import InteractionsClient
from api.interaction_types import (
    InteractionConfig, InteractionInput, AgentOption, DeepResearchAgentConfig
)

# Setup Logging
logger = logging.getLogger("DeepResearchLab")
logging.basicConfig(level=logging.INFO)

def main():
    if len(sys.argv) < 2:
        print("Usage: python deep_research_lab.py \"Your Research Query\"")
        print("Example: python deep_research_lab.py \"Future of Solid State Batteries\"")
        return

    query = sys.argv[1]
    
    print("🔬 Deep Research Lab 🔬")
    print(f"Topic: {query}")
    print("-------------------------")

    client = InteractionsClient()
    
    # Configure for Deep Research Agent
    config = InteractionConfig(
        agent=AgentOption.DEEP_RESEARCH,
        agent_config=DeepResearchAgentConfig()
    )
    
    input_data = InteractionInput(text=query)
    
    try:
        # Create Interaction
        print("Initializing Research Agent (this may take time)...")
        initial_response = client.create_interaction(input_data, config)
        interaction_id = initial_response.get("id")
        print(f"Interaction ID: {interaction_id}")
        
        # Wait for completion (Deep Research takes time!)
        final_result = client.wait_for_completion(interaction_id, poll_interval=5)
        
        print("\n✅ Research Completed!")
        print("-------------------------")
        report = client.list_outputs(final_result)
        print(report)
        
        # Optional: Save to file
        filename = f"research_{interaction_id}.md"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"\nReport saved to {filename}")

    except Exception as e:
        logger.error(f"Research failed: {e}")

if __name__ == "__main__":
    main()
