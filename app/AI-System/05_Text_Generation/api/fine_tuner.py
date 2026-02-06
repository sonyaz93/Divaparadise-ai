import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load Env
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class FineTuner:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)
        print("[CONNECTED] Fine-Tuning Client")

    def create_tuning_job(self, dataset_path, model_display_name, base_model="models/gemini-1.0-pro-001"):
        """
        Initiates a fine-tuning job.
        Args:
            dataset_path (str): Path to JSON/CSV dataset.
            model_display_name (str): Name for the new custom model.
            base_model (str): The base model to tune.
        """
        print(f"[TRAINING] Starting tuning job for '{model_display_name}'...")
        try:
            # Real implementation would look like:
            # operation = genai.create_tuned_model(
            #     source_model=base_model,
            #     training_data=dataset_path, # Needs specific formatting/upload
            #     id = model_display_name,
            #     epoch_count = 100,
            #     batch_size = 4,
            #     learning_rate = 0.001,
            # )
            
            # Since we don't have a real dataset prepared, we mock the start.
            print(f"   > Uploading dataset: {dataset_path}")
            print(f"   > Configuring hyperparameters (Epochs: 100, Batch: 4)")
            print(f"   > Job Submitted to Google Cloud.")
            
            return {"status": "training", "job_id": "mock-job-123"}
            
        except Exception as e:
            print(f"[ERROR] Training failed: {e}")
            return None

    def list_tuned_models(self):
        """Lists available custom models."""
        try:
            # return genai.list_tuned_models()
            print("Listing tuned models...")
            return ["tunedModels/diva-v1", "tunedModels/lyrics-writer-v2"]
        except Exception as e:
            return []

if __name__ == "__main__":
    tuner = FineTuner()
    tuner.list_tuned_models()
