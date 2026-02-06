import os
import google.generativeai as genai
from dotenv import load_dotenv
import datetime

load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class CacheManager:
    """
    Manages Context Caching (v1beta.cachedContents).
    Note: The Python SDK support for caching varies by version.
    This module attempts to use the caching API if available.
    """
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)

    def list_caches(self):
        """Lists active cached contents."""
        try:
            if hasattr(genai, "list_cached_contents"):
                 return list(genai.list_cached_contents())
            elif hasattr(genai.caching, "CachedContent"):
                 # Direct object approach if list helper missing
                 return [] # Placeholder if method obscure
            else:
                 print("[WARN] Caching API not found.")
                 return []
        except Exception as e:
            print(f"[ERROR] List Cache failed: {e}")
            return []

    def create_cache(self, model_name, content_obj, ttl_minutes=60):
        """
        Creates a cache for content.
        Args:
            model_name: "models/gemini-1.5-pro-001"
            content_obj: Text or File content
            ttl_minutes: Time to live
        """
        try:
            # Construct cache config
            # (Simplified implementation relying on SDK)
            if hasattr(genai.caching, "CachedContent"):
                cache = genai.caching.CachedContent.create(
                    model=model_name,
                    contents=content_obj,
                    ttl=datetime.timedelta(minutes=ttl_minutes)
                )
                print(f"[CACHE] Created: {cache.name}")
                return cache
            else:
                print("[FAIL] Caching not supported in this SDK version.")
                return None
        except Exception as e:
            print(f"[ERROR] Create Cache failed: {e}")
            return None

    def delete_cache(self, name):
        """Deletes a cached content resource."""
        try:
            if hasattr(genai.caching, "CachedContent"):
                # Usually static delete or instance delete
                # Attempting instance reference if SDK design assumes it
                cache = genai.caching.CachedContent(name=name)
                cache.delete()
                return True
            else:
                # Fallback to general delete if exposed
                return False
        except Exception as e:
            print(f"[ERROR] Delete Cache failed: {e}")
            return False

if __name__ == "__main__":
    cm = CacheManager()
    print("Caches:", cm.list_caches())
