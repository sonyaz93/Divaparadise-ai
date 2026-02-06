import sys
import os
import glob

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from text_client import TextClient

def read_codebase(root_dir):
    """
    Reads all Python and Markdown files in the directory recursively.
    """
    content = ""
    print(f"[SCAN] Reading codebase from: {root_dir}")
    
    files = glob.glob(os.path.join(root_dir, "**", "*.py"), recursive=True)
    files += glob.glob(os.path.join(root_dir, "**", "*.md"), recursive=True)
    
    for file_path in files:
        # Skip venv or cache
        if "__pycache__" in file_path or ".git" in file_path:
            continue
            
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content += f"\n\n--- FILE: {os.path.basename(file_path)} ---\n"
                content += f.read()
        except:
            pass
            
    return content

def main():
    print("[INFO] Initializing Long Context Lab 🧠...")
    client = TextClient()
    
    # 1. Ingest Data
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")) # AI-System Root
    codebase = read_codebase(target_dir)
    print(f"[DATA] Ingested {len(codebase)} characters of code.")
    
    # 2. Creating Cache
    # We treat the codebase as a "Book" that the AI studies.
    print("[CACHE] Uploading to Gemini Memory (TTL 5 mins)...")
    cache = client.create_cache(codebase, ttl_minutes=5)
    
    # 3. Querying
    prompt = """
    You are the Lead Artchitect of this system.
    Analyze the codebase structure. 
    1. List all the Modules (folders like 01_, 02_).
    2. Explain how the 'TextClient' in 05_Text_Generation is reused in 07_Function_Calling.
    3. Suggest one improvement for the architecture.
    """
    
    print("\n--- QUERYING GIANT CONTEXT ---\n")
    response = client.generate_with_cache(prompt, cache)
    print(f"[RESPONSE]:\n{response}")

if __name__ == "__main__":
    main()
