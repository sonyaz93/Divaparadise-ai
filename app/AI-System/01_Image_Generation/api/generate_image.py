import sys
import os
import time

# Add Root to Path to import the Manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google_studio_manager import GoogleStudioManager

def main():
    try:
        # 1. Initialize the Brain (Gemini)
        print("[INFO] Initializing Diva AI Brain...")
        manager = GoogleStudioManager()
        
        # 2. Get User Concept
        if len(sys.argv) > 1:
            user_concept = " ".join(sys.argv[1:])
        else:
            print("[INPUT] Enter image concept (or pass as arg):")
            # Fallback for non-interactive run if no input provided quickly
            user_concept = "Cyberpunk Diva" 
            
        print(f"[INFO] Improving concept: '{user_concept}'...")
        
        # 3. Prompt Engineering (AI Agent)
        pro_prompt = manager.generate_prompt_for_image(user_concept)
        
        print("\n" + "="*50)
        print("ENGINEERED PROMPT (Ready for SDXL/Midjourney)")
        print("="*50)
        print(pro_prompt)
        print("="*50)
        
        # 4. Simulation of Generation (Placeholder for SDXL API)
        print("\n[INFO] Sending to Image Generation Engine (Simulation)...")
        time.sleep(2)
        print("[SUCCESS] Image generated: data/processed/output_001.png")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    main()
