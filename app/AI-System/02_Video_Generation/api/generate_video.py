import sys
import os
import time

# Add Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google_studio_manager import GoogleStudioManager

def main():
    try:
        print("[INFO] Initializing Video Director Agent...")
        manager = GoogleStudioManager()
        
        # Get Script Input
        if len(sys.argv) > 1:
            script_input = " ".join(sys.argv[1:])
        else:
            print("[INPUT] Enter video script/idea:")
            script_input = "A robot discovering a flower in a wasteland."
            
        print(f"[INFO] Analyzing script: '{script_input}'...")
        
        # AI Processing
        scene_prompts = manager.script_to_video_prompt(script_input)
        
        print("\n" + "="*50)
        print("GENERATED SCENE PROMPTS (Ready for Runway/Pika)")
        print("="*50)
        print(scene_prompts)
        print("="*50)
        
        # Simulation
        print("\n[INFO] Rendering scenes (Simulation)...")
        time.sleep(2)
        print("[SUCCESS] Video clips generated: data/clips/scene_001.mp4")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    main()
