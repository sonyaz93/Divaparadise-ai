import sys
import os

# Add Path to 05 module to reuse TextClient
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../05_Text_Generation/api")))
from text_client import TextClient

# Import Tools
from tools_library import ALL_TOOLS

class AgentOrchestrator:
    def __init__(self, model_name="gemini-2.0-flash-exp"):
        self.client = TextClient(model_name=model_name)
        self.tools = ALL_TOOLS
        print(f"[ORCHESTRATOR] Initialized with {len(self.tools)} tools.")

    def run_task(self, prompt):
        """
        Runs a task using the Agentic Loop (Reasoning + Tools).
        """
        print(f"\n[AGENT] Received Task: {prompt}")
        
        # We use the thinking_budget if we want reasoning, 
        # BUT note that mixing Thinking + Tools is a Gemini 2.5/3.0 feature.
        # We will use valid config from our updated TextClient.
        
        response = self.client.generate_text(
            prompt,
            tools=self.tools,
            thinking_budget=1024 # Enable reasoning too!
        )
        
        return response

if __name__ == "__main__":
    agent = AgentOrchestrator()
    res = agent.run_task("What is 150 * 3, and what time is it right now?")
    print(f"\n[FINAL ANSWER]: {res}")
