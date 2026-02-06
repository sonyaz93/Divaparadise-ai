import sys
import os
import argparse

# Appending Paths to access sibling modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../05_Text_Generation/api")))

from audio_client import AudioGenerator
from text_client import TextClient

def main():
    print("[INFO] Initializing Podcast Studio 🎙️...")
    
    # Defaults
    topic = "The Rise of AI Music"
    host1 = {"name": "Nova", "voice": "Puck"}   # Upbeat
    host2 = {"name": "Zen", "voice": "Charon"}  # Deep/Informative
    
    if len(sys.argv) > 1:
        topic = sys.argv[1]

    # 1. Generate Script
    print(f"\n--- PHASE 1: SCRIPTING ({topic}) ---")
    writer = TextClient()
    
    prompt = (
        f"Write a short, engaging 2-person podcast script about '{topic}'. "
        f"Characters: {host1['name']} (Energetic/Fun) and {host2['name']} (Calm/Expert). "
        "Format the output exactly like this:\n"
        f"{host1['name']}: Text...\n"
        f"{host2['name']}: Text...\n"
        "Keep it under 100 words total. No sound effects cues."
    )
    
    script = writer.generate_text(prompt, temperature=0.8)
    if not script:
        print("[FAIL] Script generation failed.")
        return
        
    print("\n--- GENERATED SCRIPT ---")
    print(script)
    
    # 2. Synthesize Audio
    print(f"\n--- PHASE 2: RECORDING (Grimini TTS) ---")
    audio = AudioGenerator()
    
    # Ensure Output Dir
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/output"))
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"podcast_{topic.replace(' ', '_')}.wav")
    
    speakers = [host1, host2]
    result = audio.generate_podcast(script, speakers, output_path)
    
    if result:
        print(f"\n[SUCCESS] Podcast published to: {result}")
    else:
        print("\n[FAIL] Recording failed.")

if __name__ == "__main__":
    main()
