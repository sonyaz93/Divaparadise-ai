import requests
import json
import logging
import os
import time
from typing import Dict, Any, Optional, List
from .batch_types import BatchRequestInput, BatchState

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("BatchClient")

class BatchClient:
    """
    Client for the Gemini Batch API (v1beta).
    """
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required.")
        self.headers = {
            "Content-Type": "application/json"
        }

    def create_batch(self, 
                     model: str, 
                     input_data: BatchRequestInput, 
                     display_name: str = "batch_job") -> Dict[str, Any]:
        """
        Creates a new batch job.
        Target: models/{model}:batchGenerateContent
        """
        url = f"{self.BASE_URL}/{model}:batchGenerateContent?key={self.api_key}"
        
        payload = {
            "batch": {
                "displayName": display_name,
                "inputConfig": input_data.to_dict()
            }
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error creating batch: {e.response.text}")
            raise

    def list_batches(self) -> List[Dict[str, Any]]:
        """
        Lists all batches.
        Target: batches
        """
        url = f"{self.BASE_URL}/batches?key={self.api_key}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("batches", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error listing batches: {e.response.text}")
            return []

    def get_batch(self, batch_name: str) -> Dict[str, Any]:
        """
        Gets a specific batch status.
        Batch name format: batches/12345
        """
        url = f"{self.BASE_URL}/{batch_name}?key={self.api_key}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error getting batch: {e.response.text}")
            raise

    def cancel_batch(self, batch_name: str):
        """
        Cancels a batch.
        """
        url = f"{self.BASE_URL}/{batch_name}:cancel?key={self.api_key}"
        try:
            requests.post(url, headers=self.headers)
        except Exception as e:
            logger.error(f"Error cancelling batch: {e}")

    def monitor_batch(self, batch_name: str, poll_interval: int = 10) -> Dict[str, Any]:
        """
        Polls batch until terminal state.
        """
        logger.info(f"Monitoring batch {batch_name}...")
        while True:
            batch = self.get_batch(batch_name)
            state = batch.get("state")
            logger.info(f"State: {state} | Success: {batch.get('batchStats', {}).get('successfulRequestCount', 0)}")
            
            if state in [BatchState.SUCCEEDED.value, BatchState.FAILED.value, BatchState.CANCELLED.value]:
                return batch
            
            time.sleep(poll_interval)
