import asyncio
import logging
import sys
import os

# Adjust path to import from api
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.live_client import LiveClient
from api.session_config import SessionConfig
from api.stream_manager import AudioStream

# Setup Logging
logger = logging.getLogger("LiveLab")
logging.basicConfig(level=logging.INFO)

async def main():
    print("⚡ Gemini Live API Lab ⚡")
    print("-------------------------")
    print("Press Ctrl+C to exit.\n")

    # 1. Initialize Client & Config
    client = LiveClient()
    config = SessionConfig(
        system_instruction="You are a witty AI companion. You reply briefly and with humor.",
        generation_config={
            "responseModalities": ["AUDIO"],
            "speechConfig": {
                "voiceConfig": {"prebuiltVoiceConfig": {"voiceName": "Puck"}}
            }
        }
    )
    
    # 2. Connect
    await client.connect()
    
    # 3. Send Setup
    await client.send_setup(config.get_setup_payload())
    
    # 4. Initialize Audio Stream
    audio_stream = AudioStream()
    audio_stream.start_input()
    audio_stream.start_output()

    # 5. Define Tasks
    async def send_audio_loop():
        try:
            async for chunk in audio_stream.record_chunks():
                if not client.session_active:
                    break
                await client.send_audio_chunk(chunk)
        except Exception as e:
            logger.error(f"Error in send loop: {e}")

    async def receive_loop():
        try:
            async for msg in client.receive():
                # specific handling for server content
                if "serverContent" in msg:
                    content = msg["serverContent"]
                    # Check for model Turn
                    if "modelTurn" in content:
                        parts = content["modelTurn"].get("parts", [])
                        for part in parts:
                            if "text" in part:
                                print(f"🤖: {part['text']}")
                            if "inlineData" in part:
                                # Play audio if present
                                mime = part["inlineData"].get("mimeType")
                                data = part["inlineData"].get("data")
                                if mime.startswith("audio") and data:
                                    await audio_stream.play_audio(data)

                elif "toolCall" in msg:
                    print(f"🛠️ Tool Call: {msg['toolCall']}")
                    
        except Exception as e:
            logger.error(f"Error in receive loop: {e}")

    # 6. Run Loops
    try:
        await asyncio.gather(send_audio_loop(), receive_loop())
    except KeyboardInterrupt:
        print("\nExiting...")
    finally:
        audio_stream.stop()
        await client.close()

if __name__ == "__main__":
    asyncio.run(main())
