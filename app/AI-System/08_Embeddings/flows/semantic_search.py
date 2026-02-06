import sys
import os
import math

# Add Path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from embedding_client import EmbeddingClient

def cosine_similarity(v1, v2):
    """
    Calculates cosine similarity between two vectors.
    """
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    
    if magnitude_v1 == 0 or magnitude_v2 == 0:
        return 0.0
        
    return dot_product / (magnitude_v1 * magnitude_v2)

def main():
    print("[INFO] Initializing Semantic Search Lab 🧬...")
    client = EmbeddingClient()
    
    # 1. The Knowledge Base (Documents)
    documents = [
        "The quick brown fox jumps over the lazy dog.",
        "A fast auburn canine leaps across a sleepy pup.", # Semantically similar to 1
        "Python is a powerful programming language for AI.",
        "Gemini is Google's multimodal AI model.",
        "I love eating pizza on Fridays.",
        "Deep learning requires large datasets."
    ]
    
    print(f"[DATA] Embedding {len(documents)} documents...")
    doc_embeddings = client.embed_batch(documents, task_type="retrieval_document")
    
    # 2. The Query
    query = "coding tools for artificial intelligence"
    print(f"[QUERY] '{query}'")
    
    query_embedding = client.embed_text(query, task_type="retrieval_query")
    
    # 3. Search (Cosine Similarity)
    print("\n--- SEARCH RESULTS ---")
    results = []
    
    if doc_embeddings and query_embedding:
        for i, doc_vec in enumerate(doc_embeddings):
            score = cosine_similarity(query_embedding, doc_vec)
            results.append((score, documents[i]))
            
        # Sort by score desc
        results.sort(key=lambda x: x[0], reverse=True)
        
        for score, text in results:
            bar = "█" * int(score * 20)
            print(f"{score:.4f} | {bar} | {text}")
            
    else:
        print("[FAIL] Could not generate embeddings.")

if __name__ == "__main__":
    main()
