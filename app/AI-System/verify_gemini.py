import os
import google.generativeai as genai
from dotenv import load_dotenv

def verify_gemini():
    print("🔍 Testing Gemini API Connection...")
    
    # Load .env file
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ Error: No API Key found.")
        print("Please set a valid GEMINI_API_KEY in app/AI-System/.env")
        return
    
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash-lite')
        
        print(f"📡 Sending test request for Gemini 2.5 Flash Lite with key: {api_key[:10]}...")
        response = model.generate_content("Hello, are you working?")
        
        print("✅ Success! Gemini responded:")
        print(f"--- \n{response.text.strip()}\n---")
        
    except Exception as e:
        print(f"❌ Connection Failed: {str(e)}")
        print("\nPossible issues:")
        print("1. API Key is invalid or expired.")
        print("2. Network/VPN is blocking Google API (generativelanguage.googleapis.com).")
        print("3. Python environment needs dependency update (pip install google-generativeai).")

if __name__ == "__main__":
    verify_gemini()
