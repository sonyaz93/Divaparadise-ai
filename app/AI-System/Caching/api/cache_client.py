import requests
import json
import logging
import os
from typing import Dict, Any, Optional, List
from .cache_types import CachedContentConfig, UpdateCacheConfig

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("CacheClient")

class CacheClient:
    """
    Client for the Gemini Caching API (v1beta).
    """
    BASE_URL = "https://generativelanguage.googleapis.com/v1beta"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required.")
        self.headers = {
            "Content-Type": "application/json"
        }

    def create_cache(self, config: CachedContentConfig) -> Dict[str, Any]:
        """
        Creates a new cached content resource.
        """
        url = f"{self.BASE_URL}/cachedContents?key={self.api_key}"
        try:
            payload = config.to_dict()
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error creating cache: {e.response.text}")
            raise

    def list_caches(self, page_size: int = 50) -> List[Dict[str, Any]]:
        """
        Lists all cached contents.
        """
        url = f"{self.BASE_URL}/cachedContents?key={self.api_key}&pageSize={page_size}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            data = response.json()
            return data.get("cachedContents", [])
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error listing caches: {e.response.text}")
            return []

    def get_cache(self, name: str) -> Dict[str, Any]:
        """
        Gets a specific cached content.
        Name format: cachedContents/{id}
        """
        url = f"{self.BASE_URL}/{name}?key={self.api_key}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error getting cache: {e.response.text}")
            raise

    def update_cache(self, name: str, config: UpdateCacheConfig) -> Dict[str, Any]:
        """
        Updates the expiration of a cache.
        """
        url = f"{self.BASE_URL}/{name}?key={self.api_key}"
        try:
            payload = config.to_dict()
            response = requests.patch(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error updating cache: {e.response.text}")
            raise

    def delete_cache(self, name: str):
        """
        Deletes a cached content resource.
        """
        url = f"{self.BASE_URL}/{name}?key={self.api_key}"
        try:
            requests.delete(url, headers=self.headers)
            logger.info(f"Deleted cache: {name}")
        except Exception as e:
            logger.error(f"Error deleting cache: {e}")

    def generate_content_with_cache(self, model: str, cache_name: str, prompt: str) -> Dict[str, Any]:
        """
        Helper method to generate content using a cache.
        """
        url = f"{self.BASE_URL}/{model}:generateContent?key={self.api_key}"
        payload = {
            "contents": [{"role": "user", "parts": [{"text": prompt}]}],
            "cachedContent": cache_name
        }
        try:
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP Error generating content: {e.response.text}")
            raise
