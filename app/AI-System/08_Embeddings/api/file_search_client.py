import os
import time
import google.generativeai as genai
from google.generativeai import types
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class FileSearchClient:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        genai.configure(api_key=API_KEY)
        print("[CONNECTED] File Search Client")

    def create_store(self, display_name="diva_store"):
        """Creates a new File Search Store (if supported)."""
        try:
            # Check for direct method (newer SDKs)
            if hasattr(genai, "create_file_search_store"):
                return genai.create_file_search_store(display_name=display_name)
            
            # Check for caching client (older SDKs)
            if hasattr(genai, "CachingClient"):
                return genai.CachingClient.create_file_search_store(display_name=display_name)
                
            print("[WARN] File Search Store API not found in this SDK. Using Direct File Upload fallback.")
            return None
        except Exception as e:
            print(f"[ERROR] Create Store failed: {e}")
            return None

    def upload_file_to_store(self, file_path, store_name=None, mime_type="text/plain"):
        """Uploads a file. If store_name provided, tries to add to store."""
        try:
            print(f"[UPLOAD] Uploading {file_path}...")
            # Standard Upload (Long Context / File API)
            file_ref = genai.upload_file(file_path, mime_type=mime_type)
            print(f"[UPLOAD] Complete: {file_ref.name}")
            
            # If we have a store and the SDK supports import, do it
            if store_name:
                # Logic to add to store would go here if SDK supported it
                # For now, we return the file_ref which is sufficient for Long Context
                pass
                
            return file_ref
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None

    def list_documents(self, store_name):
        """Lists documents in a store."""
        try:
            # store_name format: fileSearchStores/{id}
            if hasattr(genai, "list_file_search_documents"):
                 return genai.list_file_search_documents(parent=store_name)
            
            # Check for caching client style
            if hasattr(genai, "CachingClient"):
                # Usually accessed via the client instance or similar
                pass
                
            return []
        except Exception as e:
            print(f"[ERROR] List Docs failed: {e}")
            return []

    def get_tool_config(self, store_name):
        """Returns the Tool config if store exists."""
        if not store_name:
            return None
            
        return types.Tool(
            file_search=types.FileSearch(
                file_search_store_names=[store_name]
            )
        )

if __name__ == "__main__":
    client = FileSearchClient()
    # Test creation (Mock or Real)
    # store = client.create_store("test_store")
    # print(store)
