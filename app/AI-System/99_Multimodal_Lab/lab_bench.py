import sys
import os
import time

# Add Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../05_Text_Generation")))

from google_studio_manager import GoogleStudioManager

def main():
    try:
        print("[INFO] Initializing Multimodal Lab 🧪...")
        lab = GoogleStudioManager()
        
        print("\nCOMMANDS:")
        print("1. list  - List active files")
        print("2. clean - Delete all files")
        print("3. test  - Run dummy multimodal test")
        
        cmd = "list"
        if len(sys.argv) > 1:
            cmd = sys.argv[1]
            
        if cmd == "list":
            lab.list_media()
            
        elif cmd == "chat":
            print("[TEST] Text Generation & Chat 💬...")
            from api.text_client import TextClient
            
            # Initialize with persona
            client = TextClient(system_instruction="You are a sarcastic robot.")
            chat = client.start_chat()
            
            print("Chat started (type 'exit' to quit):")
            while True:
                user_msg = input("You: ")
                if user_msg.lower() == "exit": break
                
                resp = chat.send_message(user_msg)
                print(f"Bot: {resp.text}")

        elif cmd == "thinking":
            # Just a placeholder test for passing config params
            print("[TEST] Thinking Model 🧠...")
             # from api.text_client import TextClient
            # client = TextClient(model="gemini-3-flash-preview")
            # print(client.generate_text("Explain quantum physics", thinking_level="low"))
            print("Thinking test implementation pending SDK verification.")

        elif cmd == "clean":
            print("[WARN] Deleting all files...")
            # Note: In production be careful.
            for f in lab.list_media(): 
                 # lab.delete_media(f.name) 
                 pass
            print("Cleanup script ready (commented out for safety).")
            
        elif cmd == "test":
            print("[TEST] simulating Multimodal Input...")
            # In a real run, we would upload an image and audio
            # img = lab.upload_media("path/to/img.png")
            # audio = lab.upload_media("path/to/audio.mp3")
            # response = lab.model.generate_content(["Describe this fusion:", img, audio])
            print("Multimodal Test Stub: Ready for inputs.")

    except Exception as e:
        print(f"[ERROR] Lab Error: {e}")

if __name__ == "__main__":
    main()
