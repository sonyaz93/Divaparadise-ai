import sys
import os
import time

# Add 'AI-System' to Path to allow importing google_studio_manager
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google_studio_manager import GoogleStudioManager

def main():
    try:
        print("[INFO] Initializing Nano Banana Workflow...")
        manager = GoogleStudioManager()
        
        print("\n--- STEP 1: CONCEPT ---")
        if len(sys.argv) > 1:
            concept = " ".join(sys.argv[1:])
            print(f"Input: {concept}")
        else:
            concept = input("Enter image concept: ")
            
        if not concept:
            concept = "Futuristic Banana Art"

        print(f"\n[INFO] Generating Drafts with 'gemini-2.5-flash-image' (FAST)...")
        # Generate 4 variations (Simulated loop)
        for i in range(1, 5):
            print(f"  > Generating Draft #{i}...")
            result = manager.generate_image(f"Draft sketch of {concept}, variation {i}", model_type='flash')
            print(f"    {result}")
            time.sleep(0.5)
            
        print("\n--- STEP 2: SELECTION ---")
        print("Assuming Draft #2 was selected by user for refinement.")
        selected_draft = f"Draft sketch of {concept}, variation 2"
        
        print("\n--- STEP 3: FINALIZE ---")
        print(f"[INFO] Upscaling with 'gemini-3-pro-image-preview' (HIGH_RES)...")
        
        # Expand prompt first
        refined_prompt = manager.generate_prompt_for_image(selected_draft)
        print(f"  > Refined Prompt: {refined_prompt[:50]}...")
        
        # Generate Final
        final_result = manager.generate_image(refined_prompt, model_type='pro')
        print(f"  > {final_result}")
        print("\n[SUCCESS] Nano Banana Workflow Complete! Output saved to data/outputs/final_nano.png")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    main()
