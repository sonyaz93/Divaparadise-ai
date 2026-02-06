import asyncio
import logging
import sys
import os
import base64

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.music_client import MusicClient
from api.music_config import (
    MusicSessionConfig, 
    MusicGenerationConfig, 
    WeightedPrompt, 
    PlaybackControl,
    MusicGenerationMode
)
# Reusing StreamManager's AudioStream logic for playback
from api.stream_manager import AudioStream

# Setup Logging
logger = logging.getLogger("MusicLab")
logging.basicConfig(level=logging.INFO)

async def main():
    print("🎵 Lyria Live Music Lab 🎵")
    print("----------------------------")
    print("Commands:")
    print("  [play]  Start generation")
    print("  [stop]  Stop generation")
    print("  [pause] Pause generation")
    print("  [p: <text>] Set prompt (e.g., 'p: cyberpunk, heavy drums')")
    print("  [bpm: <int>] Set BPM (e.g., 'bpm: 140')")
    print("  [exit]  Quit")
    print("----------------------------\n")

    # 1. Initialize Client & Config
    client = MusicClient()
    session_mgr = MusicSessionConfig()
    
    # Initial Music State
    current_prompts = [WeightedPrompt("upbeat lofi hip hop", 1.0)]
    current_config = MusicGenerationConfig(bpm=120, temperature=1.0)

    # 2. Connect
    await client.connect()
    
    # 3. Send Setup
    await client.send_payload(session_mgr.get_setup_payload())
    
    # 4. Initialize Audio Output
    # We only need output for music
    audio_stream = AudioStream() 
    audio_stream.start_output()

    # 5. Define Tasks

    async def user_input_loop():
        """
        Reads user input from stdin asynchronously (simulated via thread)
        and sends commands to the API.
        """
        while client.session_active:
            try:
                # Use to_thread to make input() non-blocking
                cmd = await asyncio.to_thread(input, ">> ")
                cmd = cmd.strip()

                if cmd == "exit":
                    await client.close()
                    break
                
                elif cmd == "play":
                    logger.info("Sending PLAY command...")
                    # Send Prompts & Config first to ensure context is set
                    await client.send_payload(session_mgr.get_client_content_payload(current_prompts))
                    await client.send_payload(session_mgr.get_generation_config_payload(current_config))
                    await client.send_payload(session_mgr.get_playback_control_payload(PlaybackControl.PLAY))
                
                elif cmd == "pause":
                    logger.info("Sending PAUSE command...")
                    await client.send_payload(session_mgr.get_playback_control_payload(PlaybackControl.PAUSE))

                elif cmd == "stop":
                    logger.info("Sending STOP command...")
                    await client.send_payload(session_mgr.get_playback_control_payload(PlaybackControl.STOP))

                elif cmd.startswith("p:"):
                    prompt_text = cmd[2:].strip()
                    logger.info(f"Updating Prompts: {prompt_text}")
                    current_prompts[0] = WeightedPrompt(prompt_text, 1.0)
                    await client.send_payload(session_mgr.get_client_content_payload(current_prompts))
                
                elif cmd.startswith("bpm:"):
                    try:
                        new_bpm = int(cmd.split(":")[1].strip())
                        logger.info(f"Updating BPM: {new_bpm}")
                        current_config.bpm = new_bpm
                        await client.send_payload(session_mgr.get_generation_config_payload(current_config))
                    except ValueError:
                        print("Invalid BPM format.")

            except Exception as e:
                logger.error(f"Input error: {e}")
                break

    async def receive_loop():
        try:
            async for msg in client.receive():
                if "serverContent" in msg:
                    content = msg["serverContent"]
                    if "audioChunks" in content:
                        for chunk in content["audioChunks"]:
                            if "data" in chunk:
                                await audio_stream.play_audio(chunk["data"])
                    
                elif "warning" in msg:
                    print(f"⚠️ Warning: {msg['warning']}")
                
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")

    # 6. Run Loops
    try:
        await asyncio.gather(user_input_loop(), receive_loop())
    except KeyboardInterrupt:
        print("\nExiting...")
    except Exception as e:
        logger.error(f"Runtime error: {e}")
    finally:
        audio_stream.stop()
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
