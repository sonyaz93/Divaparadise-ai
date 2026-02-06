import os
import google.generativeai as genai
from dotenv import load_dotenv

def list_available_models():
    print("🔍 Comprehensive Gemini Model Check...")
    load_dotenv()
    
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ No GEMINI_API_KEY found in .env")
        return

    try:
        genai.configure(api_key=api_key)
        
        print(f"📡 Requesting accessible models for key: {api_key[:10]}...")
        
        available_models = []
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                available_models.append(m.name)
        
        if available_models:
            print("✅ Key is WORKING! You have access to these models:")
            for model in available_models:
                print(f" - {model}")
            
            print("\n💡 Recommendation: Update api_server.py to use one of the models listed above.")
        else:
            print("❌ The key is valid but has access to ZERO models for content generation.")
            
    except Exception as e:
        print(f"❌ API Call Failed: {str(e)}")
        if "API_KEY_INVALID" in str(e):
            print("\n⚠️  CONFIRMED: The API Key is invalid. Please go to https://aistudio.google.com/app/apikey to get a fresh one.")
        elif "quota" in str(e).lower():
            print("\n⚠️  Quota exceeded: This key has hit its limit.")
        else:
            print("\n⚠️  Unexpected error. Please check your network connection or VPN.")

if __name__ == "__main__":
    list_available_models()
