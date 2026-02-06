import asyncio
import base64
import logging
# Note: pyaudio might need to be installed: `pip install pyaudio`
# If not available, we will mock or fail gracefully.
try:
    import pyaudio
except ImportError:
    pyaudio = None

logger = logging.getLogger("StreamManager")

class AudioStream:
    """
    Manages Audio Input (Microphone) and Output (Speaker) streams.
    """
    def __init__(self, rate: int = 16000, chunk_size: int = 512, channels: int = 1):
        self.rate = rate
        self.chunk_size = chunk_size
        self.channels = channels
        self.p = None
        self.input_stream = None
        self.output_stream = None
        self.is_recording = False

        if pyaudio:
            self.p = pyaudio.PyAudio()
        else:
            logger.warning("PyAudio not found. Audio streaming will be disabled.")

    def start_input(self):
        """
        Starts the microphone input stream.
        """
        if not self.p:
            return
        
        self.input_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size
        )
        self.is_recording = True
        logger.info("Microphone Input Started 🎤")

    def start_output(self):
        """
        Starts the speaker output stream.
        """
        if not self.p:
            return

        self.output_stream = self.p.open(
            format=pyaudio.paInt16,
            channels=self.channels,
            rate=self.rate,
            output=True
        )
        logger.info("Speaker Output Started 🔊")

    async def record_chunks(self):
        """
        Async generator that yields base64 encoded audio chunks.
        """
        if not self.input_stream:
            return

        while self.is_recording:
            try:
                # Read raw PCM data
                # Using run_in_executor to avoid blocking the async loop
                data = await asyncio.to_thread(self.input_stream.read, self.chunk_size, exception_on_overflow=False)
                
                # Encode to base64
                b64_data = base64.b64encode(data).decode("utf-8")
                yield b64_data
                
                # Small sleep to yield control if needed, though await to_thread handles it
                # await asyncio.sleep(0.001) 
            except Exception as e:
                logger.error(f"Error recording chunk: {e}")
                break

    async def play_audio(self, b64_data: str):
        """
        Plays a chunk of base64 encoded audio.
        """
        if not self.output_stream:
            return
            
        try:
            pcm_data = base64.b64decode(b64_data)
            await asyncio.to_thread(self.output_stream.write, pcm_data)
        except Exception as e:
            logger.error(f"Error playing audio: {e}")

    def stop(self):
        """
        Stops all streams.
        """
        self.is_recording = False
        
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
            
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
            
        if self.p:
            self.p.terminate()
            
        logger.info("Audio Streams Stopped.")
