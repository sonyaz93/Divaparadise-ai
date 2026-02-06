import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class ModelRegistry:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        genai.configure(api_key=API_KEY)

    def list_models(self):
        """Lists all available Gemini models."""
        try:
            print("[REGISTRY] Fetching models...")
            models = []
            for m in genai.list_models():
                if 'generateContent' in m.supported_generation_methods:
                    models.append({
                        "name": m.name,
                        "base_model_id": getattr(m, 'base_model_id', ''),
                        "version": getattr(m, 'version', ''),
                        "display_name": m.display_name,
                        "description": m.description,
                        "input_limit": m.input_token_limit,
                        "output_limit": m.output_token_limit,
                        "supported_methods": m.supported_generation_methods,
                        "temperature": getattr(m, 'temperature', None),
                        "top_p": getattr(m, 'top_p', None),
                        "top_k": getattr(m, 'top_k', None)
                    })
            return models
        except Exception as e:
            print(f"[ERROR] List Models failed: {e}")
            return []

    def get_model(self, name):
        """Gets details for a specific model."""
        try:
            return genai.get_model(name)
        except Exception as e:
            print(f"[ERROR] Get Model failed: {e}")
            return None

if __name__ == "__main__":
    registry = ModelRegistry()
    models = registry.list_models()
    for m in models:
        print(f"- {m['display_name']} ({m['name']}) [Limit: {m['input_limit']}]")
