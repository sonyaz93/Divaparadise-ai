import sys
import os
import time

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from file_search_client import FileSearchClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../05_Text_Generation/api")))
from text_client import TextClient

def ensure_dummy_data():
    """Creates a dummy PDF/Text file for testing."""
    path = "company_policy.txt"
    with open(path, "w", encoding="utf-8") as f:
        f.write("""
        === COMPANY POLICY 2026 ===
        
        1. REMOTE WORK: All employees are allowed to work from Mars on Fridays.
        2. PETS: Cyber-dogs are permitted in the office, but must be silenced during meetings.
        3. HOLIDAYS: The 'Day of the AI' (August 29th) is a mandatory paid holiday.
        4. CAFETERIA: Soylent Green is served on Tuesdays.
        """)
    return os.path.abspath(path)

def main():
    print("[INFO] Initializing Managed RAG Lab 🗄️...")
    
    fs_client = FileSearchClient()
    text_client = TextClient() # Reusing Gen Model
    
    # 1. Create Store (Try)
    print("[STORE] Creating Vector Store...")
    store = fs_client.create_store(display_name="diva_policies")
    
    # 2. Upload File
    dummy_path = ensure_dummy_data()
    # If store creation failed (None), we pass None to upload, triggering direct file usage later
    store_name = store.name if store else None
    uploaded_file = fs_client.upload_file_to_store(dummy_path, store_name)
    
    if not uploaded_file:
        print("[FAIL] Could not upload file.")
        return

    # 3. Wait for processing
    print("Waiting for file processing...")
    time.sleep(10) 
    
    # 4. Generate
    prompt = "What is the policy regarding pets?"
    print(f"\n[USER]: {prompt}")
    
    try:
        # Strategy: Use Tool if Store exists, else use File Context (Long Context)
        if store:
            print("[METHOD] Using File Search Tool")
            tool = fs_client.get_tool_config(store.name)
            # Check if text_client.generate_text supports 'tools' properly (it should)
            response = text_client.generate_text(prompt, tools=[tool])
        else:
            print("[METHOD] Using Long Context (File Direct)")
            # Passing file URI directly to model
            # Note: generate_text in text_client accepts prompt string.
            # We bypass it to use the underlying model which supports [file, prompt] list.
            
            # access the underlying genai model object
            model = text_client.model 
            response_obj = model.generate_content([uploaded_file, prompt])
            response = response_obj.text
            
        print(f"\n[AI]: {response}")
        
    except Exception as e:
        print(f"[ERROR] Generation failed: {e}")

if __name__ == "__main__":
    main()
