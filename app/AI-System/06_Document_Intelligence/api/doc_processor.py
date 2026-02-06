import os
import time
import google.generativeai as genai
from dotenv import load_dotenv

# Load Env
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class DocProcessor:
    def __init__(self, model_name="gemini-1.5-pro"):
        """
        Gemini 1.5 Pro is recommended for Document Processing due to large context window.
        """
        if not API_KEY:
            raise ValueError("API Key not found")
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        print(f"[CONNECTED] Document Processor ({model_name})")

    def upload_document(self, file_path, display_name=None):
        """
        Uploads a PDF using the Files API.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        print(f"[UPLOAD] Uploading PDF: {file_path}")
        try:
            # Upload
            doc_file = genai.upload_file(
                path=file_path, 
                display_name=display_name or os.path.basename(file_path),
                mime_type="application/pdf"
            )
            
            # Wait for processing
            print(f"[PROCESSING] Waiting for file state... current: {doc_file.state.name}")
            while doc_file.state.name == "PROCESSING":
                time.sleep(2)
                doc_file = genai.get_file(doc_file.name)
            
            if doc_file.state.name == "FAILED":
                raise ValueError("File processing failed on Google Cloud.")
                
            print(f"[READY] Document processed: {doc_file.uri}")
            return doc_file
            
        except Exception as e:
            print(f"[ERROR] Upload error: {e}")
            return None

    def analyze_document(self, file_obj, prompt="Summarize this document."):
        """
        Analyzes a single document.
        """
        try:
            response = self.model.generate_content([file_obj, prompt])
            return response.text
        except Exception as e:
            return f"Analysis Error: {e}"

    def compare_documents(self, file_objs, prompt="Compare these documents."):
        """
        Analyzes multiple documents (up to context limit).
        """
        try:
            content = [prompt] + file_objs
            response = self.model.generate_content(content)
            return response.text
        except Exception as e:
            return f"Comparison Error: {e}"

if __name__ == "__main__":
    proc = DocProcessor()
    print("Document Processor Ready.")
