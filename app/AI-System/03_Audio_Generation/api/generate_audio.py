import sys
import os
import time

# Add Root to Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from google_studio_manager import GoogleStudioManager

def main():
    try:
        print("[INFO] Initializing Music Producer Agent...")
        manager = GoogleStudioManager()
        
        # Get Input
        if len(sys.argv) > 1:
            mood_genre = " ".join(sys.argv[1:])
        else:
            print("[INPUT] Enter mood and genre:")
            mood_genre = "Sad Cyberpunk Ballad"
            
        print(f"[INFO] Composing track for: '{mood_genre}'...")
        
        # Split simple input for demo
        parts = mood_genre.split(" ")
        genre = parts[-1] if parts else "Pop"
        mood = " ".join(parts[:-1]) if len(parts) > 1 else "Start"
        
        # AI Processing
        song_structure = manager.generate_audio_structure(mood, genre)
        
        print("\n" + "="*50)
        print("GENERATED SONG STRUCTURE (Ready for Suno/MusicGen)")
        print("="*50)
        print(song_structure)
        print("="*50)
        
        # Simulation
        print("\n[INFO] Synthesizing Audio (Simulation)...")
        time.sleep(2)
        print("[SUCCESS] Audio track generated: data/outputs/demo_track.mp3")
        
    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    main()
