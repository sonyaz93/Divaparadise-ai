import sys
import os

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from model_registry import ModelRegistry
from media_handler import MediaHandler
from cache_manager import CacheManager

from token_manager import TokenManager

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    registry = ModelRegistry()
    media = MediaHandler()
    token_mgr = TokenManager()
    # cache = CacheManager()

    while True:
        print("\n=== GENERATIVE LANGUAGE ADMIN 🌐 ===")
        print("1. List Models")
        print("2. List Files")
        print("3. Count Tokens (Text/File)")
        print("4. Upload File")
        print("9. Exit")
        
        choice = input("Select: ")
        
        if choice == '1':
            print("\n--- AVAILABLE MODELS ---")
            models = registry.list_models()
            for m in models:
                print(f"ID: {m['name']}")
                print(f"Name: {m['display_name']}")
                print(f"Limits: In={m['input_limit']}, Out={m['output_limit']}")
                print(f"Defaults: Temp={m['temperature']}, TopP={m['top_p']}")
                print("-" * 20)
                
        elif choice == '2':
            print("\n--- CLOUD FILES ---")
            files = media.list_files()
            if not files:
                print("No files found.")
            for f in files:
                print(f"[{f['state']}] {f['display_name']} ({f['name']}) - {f['mime_type']}")
        
        elif choice == '3':
            sub = input("Type 't' for text or 'f' for file: ").lower()
            if sub == 't':
                txt = input("Enter text: ")
                c = token_mgr.count_tokens(txt)
                print(f"Token Count: {c}")
            elif sub == 'f':
                fp = input("Enter file path: ")
                c = token_mgr.count_file_tokens(fp)
                print(f"File Token Count: {c}")

        elif choice == '4':
            path = input("Enter absolute file path: ")
            if os.path.exists(path):
                media.upload_media(path)
            else:
                print("File not found.")

        elif choice == '9':
            break

if __name__ == "__main__":
    main_menu()
