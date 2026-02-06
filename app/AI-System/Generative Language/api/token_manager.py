import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class TokenManager:
    """
    Manages Token Counting (v1beta.models.countTokens).
    Essential for cost estimation and context window management.
    """
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)

    def count_tokens(self, text, model_name="models/gemini-1.5-flash"):
        """
        Counts tokens for a given text string.
        Args:
            text: Single string or list of strings/parts.
            model_name: Model to use for tokenization.
        """
        try:
            model = genai.GenerativeModel(model_name)
            response = model.count_tokens(text)
            return response.total_tokens
        except Exception as e:
            print(f"[ERROR] Count Tokens failed: {e}")
            return -1

    def count_file_tokens(self, file_path, model_name="models/gemini-1.5-flash"):
        """
        Counts tokens for a local file (text).
        """
        try:
            if not os.path.exists(file_path):
                print("File not found.")
                return 0
            
            with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
            
            return self.count_tokens(content, model_name)
        except Exception as e:
            print(f"[ERROR] File Count failed: {e}")
            return -1

if __name__ == "__main__":
    tm = TokenManager()
    count = tm.count_tokens("Hello world, this is a token check.")
    print(f"Tokens: {count}")
