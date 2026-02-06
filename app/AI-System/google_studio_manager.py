import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables (API Key)
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")

API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class GoogleStudioManager:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        
        genai.configure(api_key=API_KEY)
        # Using gemini-2.5-pro (latest stable)
        self.model = genai.GenerativeModel('gemini-2.5-pro')
        print("[CONNECTED] Google AI Studio (Gemini 2.5 Pro)")

    # --- FILES API (Centralized Media Management) ---
    def upload_media(self, file_path, mime_type=None):
        """Uploads a file to Google AI Studio."""
        print(f"[UPLOAD] Uploading: {file_path}")
        try:
            sample_file = genai.upload_file(path=file_path, mime_type=mime_type)
            print(f"[SUCCESS] File uploaded: {sample_file.name}")
            return sample_file
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None

    def list_media(self):
        """Lists all uploaded files."""
        print("\n--- ACTIVE FILES ---")
        try:
            for f in genai.list_files():
                print(f"Name: {f.name}, URI: {f.uri}")
        except Exception as e:
            print(f"[ERROR] List failed: {e}")

    def delete_media(self, file_name):
        """Deletes a file by name (e.g., 'files/...')"""
        try:
            genai.delete_file(file_name)
            print(f"[DELETED] {file_name}")
        except Exception as e:
            print(f"[ERROR] Delete failed: {e}")
            
    def get_media_metadata(self, file_name):
        """Gets metadata for a specific file."""
        try:
            return genai.get_file(file_name)
        except Exception as e:
            print(f"[ERROR] Get failed: {e}")
            return None

    # --- GENERATION METHODS ---

    def generate_prompt_for_image(self, concept):
        """
        Uses Gemini to design a detailed image generation prompt.
        """
        response = self.model.generate_content(
            f"Act as a professional prompt engineer. Create a detailed prompt for an image generator (like Midjourney/Stable Diffusion) based on this concept: '{concept}'. Output ONLY the prompt."
        )
        return response.text.strip()

    def analyze_image(self, image_path):
        """
        Uses Gemini Vision to analyze an input image for image-to-image workflows.
        """
        if not os.path.exists(image_path):
            return "Image not found."
            
        # In a real scenario, we would upload the file or pass bytes
        # sample_file = genai.upload_file(path=image_path)
        # response = self.model.generate_content(["Describe this image in detail for recreation:", sample_file])
        return "Comparison/Analysis Logic Placeholder"

    def script_to_video_prompt(self, script_text):
        """
        Converts a script into a scene-by-scene video generation prompt.
        """
        response = self.model.generate_content(
            f"Convert this script into a list of video generation prompts for each scene:\n\n{script_text}"
        )
        return response.text

    def generate_audio_structure(self, mood, genre):
        """
        Composes a song structure (Lyrics + Chord Progression) based on mood/genre.
        """
        response = self.model.generate_content(
            f"Act as a professional music producer. Create a song structure (Verse 1, Chorus, Verse 2) with Lyrics and suggested Chord Progressions for a '{mood}' song in the '{genre}' genre."
        )
        return response.text

    def generate_image(self, prompt, model_type='flash'):
        """
        Generates an image using Gemini Image Generation models.
        Args:
            prompt (str): The image description.
            model_type (str): 'flash' (gemini-2.5-flash) or 'pro' (gemini-3-pro-image-preview).
        """
        model_id = 'gemini-2.5-flash' if model_type == 'flash' else 'gemini-3-pro-image-preview'
        
        try:
            # Note: This uses the specific image generation prototype structure.
            # Configuring the specific model for this request
            image_model = genai.GenerativeModel(model_id)
            
            # The API call for image generation might differ slightly based on the library version,
            # using the standard generate_content with image requirements if applicable,
            # or simulating the 'Imagen' protocol if wrapped.
            # For this 'Nano Banana' workflow, we assume the prompt is sent and image data returned.
            
            response = image_model.generate_content(prompt)
            
            # In a real scenario, response.parts would contain the image bytes or url.
            # Since we are simulating the specific "Nano Banana" flow without the full Image bytes capability in this text-heavy environment:
            return f"[SIMULATED IMAGE from {model_id}]: {prompt}"
            
        except Exception as e:
            return f"Error generating image with {model_id}: {e}"

if __name__ == "__main__":
    # Test the connection
    try:
        studio = GoogleStudioManager()
        print("\n--- Test: Image Prompt Generation ---")
        print(studio.generate_prompt_for_image("A futuristic cyberpunk diva concert"))
    except Exception as e:
        print(f"Error: {e}")
