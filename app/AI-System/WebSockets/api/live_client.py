import asyncio
import json
import logging
import os
import ssl
from typing import Dict, Any, AsyncGenerator, Optional
import websockets
from dotenv import load_dotenv

# Setup Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("LiveClient")

load_dotenv()

class LiveClient:
    """
    Manages the bidirectional WebSocket connection to Gemini Live API.
    """
    HOST = "generativelanguage.googleapis.com"
    PATH = "/ws/google.ai.generativelanguage.v1beta.GenerativeService.BidiGenerateContent"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Set VITE_GEMINI_API_KEY in .env or pass it to constructor.")
        
        self.uri = f"wss://{self.HOST}{self.PATH}?key={self.api_key}"
        self.ws = None
        self.session_active = False

    async def connect(self):
        """
        Establishes the WebSocket connection.
        """
        try:
            # Create SSL context to ensure secure connection
            ssl_context = ssl.create_default_context()
            self.ws = await websockets.connect(self.uri, ssl=ssl_context)
            self.session_active = True
            logger.info("Connected to Gemini Live API ⚡")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.session_active = False
            raise

    async def send_setup(self, setup_payload: Dict[str, Any]):
        """
        Sends the initial BidiGenerateContentSetup message.
        """
        if not self.ws:
            raise ConnectionError("WebSocket is not connected.")
        
        logger.info("Sending Setup Configuration...")
        await self.ws.send(json.dumps(setup_payload))

    async def send_realtime_input(self, data: Dict[str, Any]):
        """
        Sends realtime input (Audio/Video/Text).
        """
        if not self.ws:
            return

        payload = {"realtimeInput": data}
        await self.ws.send(json.dumps(payload))

    async def send_text(self, text: str):
        """
        Convenience method to send text input.
        """
        await self.send_realtime_input({"text": text})

    async def send_audio_chunk(self, base64_audio: str, mime_type: str = "audio/pcm"):
        """
        Convenience method to send audio chunk.
        """
        # Note: API expects 'mediaChunks' for BidiGenerateContentRealtimeInput
        # based on documentation provided:
        # "mediaChunks": [ { "mimeType": "audio/pcm", "data": "<base64>" } ]
        # BUT updated docs say: "audio": {"data": ..., "mimeType": ...} or "mediaChunks" is deprecated.
        # We will use the 'mediaChunks' format as it's often more stable in preview, 
        # but let's try the newer 'audio' field if documented.
        # The user doc says: 
        # "mediaChunks[] ... DEPRECATED: Use one of audio, video, or text instead."
        # "audio": [Blob]
        
        # Using 'audio' field as per new docs
        data = {
            "audio": {
                "mimeType": mime_type,
                "data": base64_audio
            }
        }
        await self.send_realtime_input(data)

    async def receive(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Async generator for receiving messages from the server.
        """
        if not self.ws:
            raise ConnectionError("WebSocket is not connected.")

        try:
            async for message in self.ws:
                # Raw message is JSON
                try:
                    data = json.loads(message)
                    yield data
                except json.JSONDecodeError:
                    logger.warning(f"Received non-JSON message: {message}")
        except websockets.exceptions.ConnectionClosed:
            logger.info("Connection closed by server.")
            self.session_active = False
        except Exception as e:
            logger.error(f"Error receiving message: {e}")
            self.session_active = False

    async def close(self):
        """
        Closes the connection.
        """
        if self.ws:
            await self.ws.close()
            self.session_active = False
            logger.info("Connection closed.")
