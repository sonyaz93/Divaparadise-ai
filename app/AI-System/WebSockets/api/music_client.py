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
logger = logging.getLogger("MusicClient")

load_dotenv()

class MusicClient:
    """
    Manages the bidirectional WebSocket connection to Lyria Live Music API.
    """
    HOST = "generativelanguage.googleapis.com"
    PATH = "/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateMusic"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("VITE_GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key is required. Set VITE_GEMINI_API_KEY in .env or pass it to constructor.")
        
        # Note the v1alpha version in the PATH
        self.uri = f"wss://{self.HOST}{self.PATH}?key={self.api_key}"
        self.ws = None
        self.session_active = False

    async def connect(self):
        """
        Establishes the WebSocket connection.
        """
        try:
            ssl_context = ssl.create_default_context()
            self.ws = await websockets.connect(self.uri, ssl=ssl_context)
            self.session_active = True
            logger.info("Connected to Lyria Music API 🎵")
        except Exception as e:
            logger.error(f"Connection failed: {e}")
            self.session_active = False
            raise

    async def send_payload(self, payload: Dict[str, Any]):
        """
        Generic send method for JSON payloads.
        """
        if not self.ws:
            logger.error("WebSocket not connected.")
            return
        
        try:
            await self.ws.send(json.dumps(payload))
        except Exception as e:
            logger.error(f"Error sending payload: {e}")

    async def receive(self) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Async generator for receiving messages from the server.
        """
        if not self.ws:
            raise ConnectionError("WebSocket is not connected.")

        try:
            async for message in self.ws:
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
        if self.ws:
            await self.ws.close()
            self.session_active = False
            logger.info("Connection closed.")
