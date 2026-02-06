import os
import time
from google.genai import Client, types
from dotenv import load_dotenv

# Load Environment Variables
# Adjust path as needed to point to your .env file
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class VideoAnalyzer:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        self.client = Client(api_key=API_KEY)
        print("[CONNECTED] Video Analyzer (Gemini Vision) Initialized")

    def upload_video(self, file_path):
        """
        Uploads a video to Google File API for processing.
        Returns the file object/URI.
        """
        print(f"[UPLOAD] Uploading video: {file_path}...")
        try:
            # Upload file
            video_file = self.client.files.upload(file=file_path)
            
            # Wait for processing state to be ACTIVE
            print("[PROCESSING] Waiting for video processing...")
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = self.client.files.get(name=video_file.name)
                
            if video_file.state.name == "FAILED":
                raise ValueError(f"Video processing failed: {video_file.state.name}")
                
            print(f"[READY] Video processed: {video_file.uri}")
            return video_file
            
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            raise e

    def analyze_video(self, video_file, prompt="Describe this video in detail."):
        """
        Analyzes an uploaded video file object with a text prompt.
        """
        print(f"[ANALYZING] Sending prompt: '{prompt}'...")
        try:
            # Using Gemini 1.5 Pro or Flash for vision tasks (2.0 if available)
            # Defaulting to 1.5 Pro for best reasoning, or Flash for speed.
            # User mentioned 'gemini-3-flash-preview' in their docs, let's try a known vision model or that ID if available.
            # Safest bet for now: 'gemini-1.5-pro' or 'gemini-2.0-flash-exp' if available.
            # Let's use 'gemini-1.5-flash' for speed/cost efficiency in this tool, or 'gemini-1.5-pro' for quality.
            model_id = "gemini-1.5-pro" 
            
            response = self.client.models.generate_content(
                model=model_id,
                contents=[
                    video_file,
                    prompt
                ]
            )
            return response.text
            
        except Exception as e:
            print(f"[ERROR] Analysis failed: {e}")
            return f"Error: {e}"

if __name__ == "__main__":
    # Test
    analyzer = VideoAnalyzer()
