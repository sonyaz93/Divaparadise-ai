import sys
import os
import time

# Add Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Add 'api' folder to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))

from veo_client import VeoClient

def main():
    try:
        print("[INFO] Initializing Veo Cinema...")
        client = VeoClient()
        
        print("\nSELECT MODE:")
        print("1. Direct (Text-to-Video)")
        print("2. Animate (Nano Banana Image -> Video)")
        
        mode = "1" # Default to 1 for non-interactive demo if needed, or read args.
        if len(sys.argv) > 1:
            # Simple arg parsing
            if "animate" in sys.argv: mode = "2"
        
        if mode == "1":
            print("\n--- MODE: DIRECT ---")
            prompt = "A cinematic drone shot of a futuristic cyberpunk city with neon rain, 4k resolution"
            if len(sys.argv) > 1 and mode == "1":
                prompt = " ".join(sys.argv[1:])
            
            output_file = "data/clips/veo_direct_shutdown.mp4"
            client.generate_video(prompt, resolution="4k", output_path=output_file)
            
        elif mode == "2":
            print("\n--- MODE: ANIMATE ---")
            # Example path from Nano Banana output
            image_path = "../../01_Image_Generation/data/outputs/final_nano.png"
            prompt = "The monkey rides the skateboard down the neon street, dynamic motion"
            
            output_file = "data/clips/veo_animated_shutdown.mp4"
            client.animate_image(image_path, prompt, output_path=output_file)

    except Exception as e:
        print(f"[ERROR] Workflow Error: {e}")

if __name__ == "__main__":
    main()
