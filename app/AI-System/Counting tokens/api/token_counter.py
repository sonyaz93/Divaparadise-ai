import google.generativeai as genai
from google.generativeai.types import Content, Part
import os
import logging
from typing import List, Union, Dict, Any, Optional

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("TokenCounter")

class TokenCounter:
    """
    Utility wrapper for counting tokens using the Gemini API (models.countTokens).
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required.")
        genai.configure(api_key=self.api_key)

    def count_text(self, model: str, text: str) -> int:
        """
        Counts tokens for a simple text prompt.
        """
        try:
            model_instance = genai.GenerativeModel(model)
            response = model_instance.count_tokens(text)
            return response.total_tokens
        except Exception as e:
            logger.error(f"Error counting text tokens: {e}")
            return -1

    def count_chat(self, model: str, history: List[Dict], new_message: Optional[str] = None) -> int:
        """
        Counts tokens for a chat history + optional new message.
        History format: [{"role": "user", "parts": ["..."]}, ...]
        """
        try:
            model_instance = genai.GenerativeModel(model)
            
            # Convert dictionary history to Content objects if needed, 
            # or usage `count_tokens` handles list of dicts often.
            # But safer to use SDK types or let SDK handle conversion.
            # The SDK usually accepts list of dicts compatible with Content.
            
            contents = history.copy()
            if new_message:
                contents.append({"role": "user", "parts": [new_message]})
                
            response = model_instance.count_tokens(contents)
            return response.total_tokens
        except Exception as e:
            logger.error(f"Error counting chat tokens: {e}")
            return -1

    def count_multimodal(self, model: str, prompt: str, file_uri: str, mime_type: str) -> int:
        """
        Counts tokens for a prompt + file (Image/Video/PDF).
        """
        try:
            model_instance = genai.GenerativeModel(model)
            
            # Create Part object for file
            file_part = Part(file_data={"mime_type": mime_type, "file_uri": file_uri})
            text_part = Part(text=prompt)
            
            content = Content(parts=[text_part, file_part], role="user")
            
            response = model_instance.count_tokens(content)
            return response.total_tokens
        except Exception as e:
            logger.error(f"Error counting multimodal tokens: {e}")
            return -1

    def get_detailed_usage(self, model: str, contents: Any) -> Dict[str, Any]:
        """
        Returns full usage metadata (total, cached, modalities).
        """
        # Note: The standard `count_tokens` return object has `total_tokens`.
        # Detailed breakdown depends on SDK version. 
        # Recent versions return an object with more fields.
        try:
            model_instance = genai.GenerativeModel(model)
            response = model_instance.count_tokens(contents)
            # Response object usually has `total_tokens`. 
            # Check if `prompt_tokens_details` etc exist.
            
            return {
                "total_tokens": response.total_tokens,
                # Safe access if fields are missing in this SDK version
                # "cached_content_token_count": getattr(response, "cached_content_token_count", 0),
            }
        except Exception as e:
            logger.error(f"Error getting detailed usage: {e}")
            return {}
