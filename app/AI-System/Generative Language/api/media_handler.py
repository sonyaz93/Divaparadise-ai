import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class MediaHandler:
    def __init__(self):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        genai.configure(api_key=API_KEY)

    def upload_media(self, file_path, mime_type=None):
        """Uploads a file to the Files API."""
        try:
            print(f"[MEDIA] Uploading {file_path}...")
            # If mime_type is provided, pass it, otherwise let SDK infer
            if mime_type:
                f = genai.upload_file(file_path, mime_type=mime_type)
            else:
                f = genai.upload_file(file_path)
            print(f"[MEDIA] Uploaded: {f.name} ({f.display_name})")
            return f
        except Exception as e:
            print(f"[ERROR] Upload failed: {e}")
            return None

    def list_files(self):
        """Lists all files in the project."""
        try:
            files = []
            for f in genai.list_files():
                files.append({
                    "name": f.name,
                    "display_name": f.display_name,
                    "mime_type": f.mime_type,
                    "size": f.size_bytes,
                    "uri": f.uri,
                    "state": f.state.name
                })
            return files
        except Exception as e:
            print(f"[ERROR] List Files failed: {e}")
            return []

    def delete_file(self, name):
        """Deletes a file by resource name."""
        try:
            genai.delete_file(name)
            print(f"[MEDIA] Deleted: {name}")
            return True
        except Exception as e:
            print(f"[ERROR] Delete failed: {e}")
            return False

if __name__ == "__main__":
    handler = MediaHandler()
    print("Files:", handler.list_files())
