import requests
import json
import logging
import os
import time
from typing import Dict, Any, Optional, Generator
from .interaction_types import InteractionConfig, InteractionInput

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("InteractionsClient")

class InteractionsClient:
    """
    Client for the Gemini Interactions API (v1beta).
    """
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta/interactions"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required.")
        self.headers = {
            "Content-Type": "application/json"
        }

    def create_interaction(self, 
                           input_data: InteractionInput, 
                           config: InteractionConfig,
                           stream: bool = False) -> Dict[str, Any]:
        """
        Creates a new interaction.
        """
        url = f"{self.BASE_URL}?key={self.api_key}"
        
        payload = config.to_dict()
        # Input handling: The API expects 'input' field which can be string or object.
        # Our InteractionInput helper creates a Turn-like structure, but let's just pass text for simplicity if needed,
        # or properly structure it.
        # API Doc: input: Content | Content[] | Turn[] | string
        
        # Taking simple string path if just text, otherwise complex.
        payload["input"] = input_data.text 
        
        if stream:
            payload["stream"] = True

        try:
            response = requests.post(url, headers=self.headers, json=payload, stream=stream)
            response.raise_for_status()
            
            if stream:
                return response # Return response object for stream handling
            else:
                return response.json()
                
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise

    def get_interaction(self, interaction_id: str) -> Dict[str, Any]:
        """
        Retrieves interaction details.
        """
        url = f"{self.BASE_URL}/{interaction_id}?key={self.api_key}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error: {e.response.text}")
            raise

    def wait_for_completion(self, interaction_id: str, poll_interval: int = 2) -> Dict[str, Any]:
        """
        Polls the interaction until status is 'completed' or 'failed'.
        Useful for long-running agents like Deep Research.
        """
        logger.info(f"Waiting for interaction {interaction_id}...")
        while True:
            data = self.get_interaction(interaction_id)
            status = data.get("status")
            
            if status == "completed":
                return data
            elif status == "failed":
                raise RuntimeError(f"Interaction failed: {data}")
            elif status == "requires_action":
                return data # Hand off to tool handler
                
            logger.info(f"Status: {status}...")
            time.sleep(poll_interval)

    def list_outputs(self, interaction_data: Dict[str, Any]) -> str:
        """
        Helper to extract text output from response.
        """
        outputs = interaction_data.get("outputs", [])
        text_parts = []
        for out in outputs:
            if out.get("type") == "text":
                text_parts.append(out.get("text", ""))
        return "\n".join(text_parts)
