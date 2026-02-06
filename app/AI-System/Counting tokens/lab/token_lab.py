import sys
import os
import logging

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.token_counter import TokenCounter

# Setup Logging
logger = logging.getLogger("TokenLab")
logging.basicConfig(level=logging.INFO)

def main():
    print("🧮 Gemini Token Counting Lab 🧮")
    print("-------------------------------")

    counter = TokenCounter()
    model = "gemini-2.0-flash-exp" # Using latest Flash model

    # 1. Text Counting
    text = "The quick brown fox jumps over the lazy dog."
    count = counter.count_text(model, text)
    print(f"\n[Text] '{text}'")
    print(f"Tokens: {count}")

    # 2. Chat History Counting
    history = [
        {"role": "user", "parts": ["Hi, I am Bob."]},
        {"role": "model", "parts": ["Hello Bob! How can I help?"]}
    ]
    new_msg = "Explain quantum physics."
    chat_count = counter.count_chat(model, history, new_msg)
    print(f"\n[Chat] History (2 turns) + New Message")
    print(f"Tokens: {chat_count}")

    # 3. Multimodal (Placeholder)
    # To run this, you need a valid file URI (uploaded via File API).
    # We will skip execution unless a URI is provided, but show how to call it.
    print(f"\n[Multimodal] (Example Code)")
    print("count = counter.count_multimodal(model, 'Describe this video', 'https://.../video.mp4', 'video/mp4')")
    
    print("\n-------------------------------")
    print("✅ Token Counting Tests Completed.")

if __name__ == "__main__":
    main()
