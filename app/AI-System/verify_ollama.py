import os
import requests
from dotenv import load_dotenv

def verify_ollama():
    print("🔍 Testing Ollama Connection...")
    load_dotenv()
    
    ollama_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model = os.getenv("OLLAMA_MODEL", "llama3")
    
    try:
        # 1. Check if Ollama is running
        response = requests.get(f"{ollama_url}/api/tags", timeout=5)
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            print(f"✅ Ollama is running! Available models: {', '.join(models)}")
            
            if ollama_model not in models:
                # Try partial match (e.g. "llama3:latest" vs "llama3")
                match = next((m for m in models if m.startswith(ollama_model)), None)
                if match:
                    print(f"ℹ️  Partial match found: using '{match}' instead of '{ollama_model}'")
                    ollama_model = match
                else:
                    print(f"⚠️  Warning: Model '{ollama_model}' not found in Ollama. Please run 'ollama pull {ollama_model}'")
                    return

            # 2. Test chat
            print(f"📡 Sending test chat to model: {ollama_model}...")
            chat_response = requests.post(
                f"{ollama_url}/api/chat",
                json={
                    "model": ollama_model,
                    "messages": [{"role": "user", "content": "Hello, respond with one word: Success."}],
                    "stream": False
                },
                timeout=30
            )
            
            if chat_response.status_code == 200:
                print("✅ Success! Ollama responded:")
                print(f"--- \n{chat_response.json()['message']['content'].strip()}\n---")
            else:
                print(f"❌ Chat failed: {chat_response.status_code} - {chat_response.text}")
        else:
            print(f"❌ Ollama returned error: {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print(f"❌ Connection Failed: Could not reach Ollama at {ollama_url}")
        print("Please make sure Ollama is installed and running.")
    except Exception as e:
        print(f"❌ An error occurred: {str(e)}")

if __name__ == "__main__":
    verify_ollama()
