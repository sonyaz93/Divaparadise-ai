import sys
import os

# Add Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
# Add 'api' folder to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))

from video_analyzer import VideoAnalyzer

def main():
    try:
        print("[INFO] Initializing Scene Analyzer...")
        analyzer = VideoAnalyzer()
        
        # Check args
        if len(sys.argv) < 2:
            print("Usage: python analyze_scene.py <video_path> [prompt]")
            return

        video_path = sys.argv[1]
        prompt = "Describe this video in detail."
        if len(sys.argv) > 2:
            prompt = " ".join(sys.argv[2:])

        if not os.path.exists(video_path):
            print(f"[ERROR] File not found: {video_path}")
            return

        # Execute Flow
        print(f"\n--- STEP 1: UPLOAD ---")
        video_file = analyzer.upload_video(video_path)
        
        print(f"\n--- STEP 2: ANALYZE ---")
        result = analyzer.analyze_video(video_file, prompt)
        
        print(f"\n--- RESULT ---")
        print(result)
        
    except Exception as e:
        print(f"[ERROR] Workflow Error: {e}")

if __name__ == "__main__":
    main()
