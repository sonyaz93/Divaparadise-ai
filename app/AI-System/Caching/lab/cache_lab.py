import sys
import os
import logging
import json
import time

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.cache_client import CacheClient
from api.cache_types import CachedContentConfig, UpdateCacheConfig

# Setup Logging
logger = logging.getLogger("CacheLab")
logging.basicConfig(level=logging.INFO)

def main():
    print("💾 Gemini Context Caching Lab 💾")
    print("--------------------------------")
    
    client = CacheClient()
    model = "models/gemini-1.5-flash-001"
    
    # 1. Create a "Large" Content Stub (Simulating a long document)
    # in practice, you'd use File API or huge text
    large_text = "This is a repeated context about the Diva System. " * 500 
    print(f"Prepared content size: {len(large_text)} chars")
    
    config = CachedContentConfig(
        model=model,
        contents=[{"role": "user", "parts": [{"text": large_text}]}],
        ttl_seconds=300, # 5 minutes
        display_name="diva_lab_cache",
        system_instruction={"parts": [{"text": "You are a helpful assistant knowing the context."}]}
    )
    
    try:
        # 2. Create Cache
        print("\nCreating Cache...")
        cache = client.create_cache(config)
        cache_name = cache.get("name")
        print(f"✅ Cache Created: {cache_name}")
        print(f"Expires: {cache.get('expireTime')}")
        print(f"Tokens: {cache.get('usageMetadata', {}).get('totalTokenCount')}")
        
        # 3. Use Cache for Generation
        print("\nQuerying using Cache...")
        response = client.generate_content_with_cache(
            model=model,
            cache_name=cache_name,
            prompt="Summarize the repeated phrase in the context."
        )
        
        # Parse Response
        try:
            answer = response["candidates"][0]["content"]["parts"][0]["text"]
            print(f"🤖 Model Answer: {answer}")
        except:
            print(f"Raw Response: {response}")
            
        # 4. List Caches
        print("\nListing Active Caches...")
        caches = client.list_caches()
        for c in caches:
            print(f"- {c.get('name')} ({c.get('displayName')})")
            
        # 5. Cleanup
        input("\nPress Enter to delete the cache and exit...")
        client.delete_cache(cache_name)
        print("✅ Cache Deleted.")

    except Exception as e:
        logger.error(f"Cache Lab Failed: {e}")

if __name__ == "__main__":
    main()
