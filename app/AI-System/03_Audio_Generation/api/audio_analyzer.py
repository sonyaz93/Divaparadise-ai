import os
import json
import time
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv

# Load Env
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class AudioAnalyzer:
    def __init__(self, model_name="gemini-2.0-flash-exp"):
        """
        Using Gemini 2.0 Flash for low latency audio analysis.
        """
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        print(f"[CONNECTED] Audio Analyzer ({model_name})")

    def upload_audio(self, file_path):
        """Uploads audio file via Files API."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
            
        print(f"[UPLOAD] Uploading audio: {file_path}...")
        audio_file = genai.upload_file(path=file_path)
        
        # Wait for processing
        while audio_file.state.name == "PROCESSING":
            time.sleep(1)
            audio_file = genai.get_file(audio_file.name)
            
        if audio_file.state.name == "FAILED":
            raise ValueError("Audio processing failed.")
            
        print(f"[READY] Audio processed: {audio_file.uri}")
        return audio_file

    def transcribe(self, file_path):
        """
        Generates a detailed transcription with speaker diarization and emotion.
        Returns a JSON object.
        """
        try:
            audio_file = self.upload_audio(file_path)
            
            prompt = """
            Analyze this audio.
            Output a JSON object with a 'segments' list.
            Each segment must have:
            - 'timestamp' (MM:SS)
            - 'speaker' (Speaker 1, 2 etc)
            - 'transcript' (The text)
            - 'emotion' (Happy, Sad, Angry, Neutral, Excited, etc)
            - 'language' (Language code e.g. en, es)
            """
            
            # Request JSON output
            config = genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
            
            response = self.model.generate_content(
                [audio_file, prompt],
                generation_config=config
            )
            
            return json.loads(response.text)
            
        except Exception as e:
            print(f"[ERROR] Transcription failed: {e}")
            return None

if __name__ == "__main__":
    analyzer = AudioAnalyzer()
    print("Audio Analyzer Ready.")
