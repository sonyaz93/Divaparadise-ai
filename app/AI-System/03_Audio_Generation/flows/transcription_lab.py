import sys
import os
import json

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from audio_analyzer import AudioAnalyzer

def main():
    print("[INFO] Initializing Transcription Lab 👂...")
    
    if len(sys.argv) < 2:
        print("Usage: python transcription_lab.py <audio_path>")
        return

    audio_path = sys.argv[1]
    
    analyzer = AudioAnalyzer()
    
    print(f"\n--- LISTENING to {os.path.basename(audio_path)} ---")
    result = analyzer.transcribe(audio_path)
    
    if result and "segments" in result:
        print("\n--- TRANSCRIPT ---")
        for seg in result["segments"]:
            ts = seg.get("timestamp", "00:00")
            spk = seg.get("speaker", "Unknown")
            emo = seg.get("emotion", "Neutral")
            text = seg.get("transcript", "")
            
            # Format: [00:12] Speaker (Happy): Text...
            print(f"[{ts}] {spk} ({emo}): {text}")
            
        # Optional: Save to .json
        out_path = audio_path + ".json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)
        print(f"\n[SAVED] JSON data saved to {out_path}")
        
    else:
        print("[FAIL] Could not transcribe audio.")

if __name__ == "__main__":
    main()
