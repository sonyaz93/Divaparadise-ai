import os
import json
import base64
import io
import numpy as np
from PIL import Image, ImageDraw
import google.generativeai as genai
from dotenv import load_dotenv

# Load Env
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class ImageIntelligence:
    def __init__(self, model_name="gemini-2.0-flash-exp"):
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        print(f"[CONNECTED] Image Intelligence ({model_name})")

    def detect_objects(self, image_path, prompt="Detect all prominent items."):
        """
        Detects objects and returns 2D bounding boxes.
        Target Model: Gemini 2.0 Flash or newer.
        """
        try:
            image = Image.open(image_path)
            
            # Request JSON output for bounding boxes
            config = genai.types.GenerationConfig(
                response_mime_type="application/json"
            )
            
            full_prompt = f"{prompt} Output a JSON list of bounding boxes with keys: box_2d [ymin, xmin, ymax, xmax] (0-1000 scale), label."
            
            response = self.model.generate_content(
                [image, full_prompt],
                generation_config=config
            )
            
            return json.loads(response.text)
        except Exception as e:
            print(f"[ERROR] Detection failed: {e}")
            return []

    def segment_objects(self, image_path, prompt="Segment the main objects."):
        """
        Segments objects and returns masks.
        Target Model: Gemini 2.5 (Thinking Budget = 0 recommended).
        """
        try:
            # Note: Segmentation often requires specifically Gemini 2.5
            # and thinking_budget=0 for efficiency/accuracy in this mode.
            
            image = Image.open(image_path)
            
            # Config for Segmentation (Disable thinking for pure vision task if using 2.5 thinking model)
            # Check SDK support for ThinkingConfig on this specific model version in future.
            # config = genai.types.GenerationConfig(
            #    thinking_config=genai.types.ThinkingConfig(thinking_budget=0)
            # )
            
            full_prompt = (
                f"{prompt} Output a JSON list where each entry contains: "
                f"'box_2d', 'label', and 'mask' (base64 png)."
            )

            response = self.model.generate_content([image, full_prompt])
            
            # Parse JSON from markdown block if present
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0]
            
            return json.loads(text)
            
        except Exception as e:
            print(f"[ERROR] Segmentation failed: {e}")
            return []

    def analyze(self, image_path, prompt):
        """Standard Visual Q&A."""
        try:
            image = Image.open(image_path)
            response = self.model.generate_content([image, prompt])
            return response.text
        except Exception as e:
            return f"Analysis failed: {e}"

if __name__ == "__main__":
    # Integration Test
    intel = ImageIntelligence()
    print("Image Intelligence Ready.")
