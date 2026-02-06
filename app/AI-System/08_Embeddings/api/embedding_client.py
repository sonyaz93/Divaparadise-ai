import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv(r"c:\Divaparadises\Divaparadises\app\.env")
API_KEY = os.getenv("VITE_GEMINI_API_KEY")

class EmbeddingClient:
    def __init__(self, model_name="models/text-embedding-004"):
        if not API_KEY:
            raise ValueError("API Key not found in .env")
        
        genai.configure(api_key=API_KEY)
        self.model_name = model_name
        print(f"[CONNECTED] Embedding Client ({model_name})")

    def embed_text(self, text, task_type="retrieval_document", title=None, output_dimensionality=None):
        """
        Embeds a single string of text.
        Args:
            text (str): Input text.
            task_type (str): Task type enum string.
            title (str): Optional title for retrieval_document.
            output_dimensionality (int): Optional vector size (e.g. 768).
        """
        try:
            # Build Config
            config = {}
            if output_dimensionality:
                config["output_dimensionality"] = output_dimensionality

            # Handle Title (Only for retrieval_document)
            content_args = {"content": text}
            if title and task_type == "retrieval_document":
                content_args["title"] = title

            result = genai.embed_content(
                model=self.model_name,
                task_type=task_type,
                **content_args,
                **config
            )
            return result['embedding']
        except Exception as e:
            print(f"[ERROR] Embedding failed: {e}")
            return None

    def embed_batch(self, texts, task_type="retrieval_document", titles=None, output_dimensionality=None):
        """
        Embeds a list of texts.
        Args:
            texts (list): List of strings.
            titles (list): List of titles (optional, must match length of texts).
        """
        try:
            config = {}
            if output_dimensionality:
                config["output_dimensionality"] = output_dimensionality

            # Note: Batch titles supported in some SDK versions, but for simplicity
            # we passing content as list. If titles provided, extensive formatting needed.
            # Keeping it simple for batch: just content.
            
            result = genai.embed_content(
                model=self.model_name,
                content=texts,
                task_type=task_type,
                **config
            )
            return result['embedding']
        except Exception as e:
            print(f"[ERROR] Batch Embedding failed: {e}")
            return None

if __name__ == "__main__":
    client = EmbeddingClient()
    vector = client.embed_text("Hello World")
    print(f"Vector Length: {len(vector)}")
