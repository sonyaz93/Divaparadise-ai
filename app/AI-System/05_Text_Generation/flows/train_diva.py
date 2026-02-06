import sys
import os
import time

# Add Paths
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))

from fine_tuner import FineTuner

def main():
    try:
        print("[INFO] Initializing Diva Training Workflow 🏋️‍♀️...")
        tuner = FineTuner()
        
        print("\n--- STEP 1: DATA PREPARATION ---")
        dataset_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/training/diva_style_v1.json"))
        
        if not os.path.exists(dataset_path):
            print(f"[WARN] Dataset not found at: {dataset_path}")
            print("       Please place your JSON training data there.")
            print("       [SIMULATION] Generating dummy dataset for test...")
            # Create dummy file if missing
            os.makedirs(os.path.dirname(dataset_path), exist_ok=True)
            with open(dataset_path, "w") as f:
                f.write('[{"text_input": "Hello", "output": "Hi Diva!"}]')
        
        print(f"[OK] Dataset ready: {dataset_path}")

        print("\n--- STEP 2: CONFIGURATION ---")
        model_name = input("Enter new model name (default: diva-v1): ") or "diva-v1"
        base_model = "models/gemini-1.5-flash-001-tuning"
        
        print(f"Target: {model_name}")
        print(f"Base: {base_model}")

        print("\n--- STEP 3: TRAINING ---")
        confirm = input("Start training job? (y/n): ")
        if confirm.lower() == 'y':
            job = tuner.create_tuning_job(dataset_path, model_name)
            if job:
                print(f"\n[SUCCESS] Job Submitted! ID: {job.get('job_id')}")
                print("Check Google AI Studio for progress.")
        else:
            print("[CANCELLED] Training aborted.")

    except Exception as e:
        print(f"[ERROR] Workflow Error: {e}")

if __name__ == "__main__":
    main()
