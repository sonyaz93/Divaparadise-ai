import sys
import os
import argparse

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from doc_processor import DocProcessor

def main():
    print("[INFO] Initializing Research Assistant 🧐...")
    
    # Simple CLI
    if len(sys.argv) < 3:
        print("Usage: python research_assistant.py <pdf_path> \"<prompt>\"")
        print("Example: python research_assistant.py my_contract.pdf \"Extract the expiration date\"")
        return # Exit if no args

    pdf_path = sys.argv[1]
    prompt = sys.argv[2]
    
    # Use Gemini 1.5 Pro (default in DocProcessor) for best Document understanding
    assistant = DocProcessor()

    # Flow
    print(f"\n--- STEP 1: UPLOAD & PROCESS ---")
    doc_file = assistant.upload_document(pdf_path)
    
    if doc_file:
        print(f"\n--- STEP 2: ANALYZE ---")
        print(f"Prompt: {prompt}")
        result = assistant.analyze_document(doc_file, prompt)
        
        print("\n--- RESULT ---")
        print(result)
    else:
        print("[FAIL] Could not process document.")

if __name__ == "__main__":
    main()
