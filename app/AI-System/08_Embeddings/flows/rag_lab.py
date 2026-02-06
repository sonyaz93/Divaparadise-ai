import sys
import os
import math

# Pathway to Modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../api")))
from embedding_client import EmbeddingClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../05_Text_Generation/api")))
from text_client import TextClient

def cosine_similarity(v1, v2):
    dot_product = sum(a * b for a, b in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(a * a for a in v1))
    magnitude_v2 = math.sqrt(sum(b * b for b in v2))
    if magnitude_v1 == 0 or magnitude_v2 == 0: return 0.0
    return dot_product / (magnitude_v1 * magnitude_v2)

def main():
    print("[INFO] Initializing RAG Lab 🧬+🧠...")
    
    embed_client = EmbeddingClient()
    text_client = TextClient()
    
    # 1. The Knowledge Base (Simulating a Vector DB)
    knowledge_base = [
        {"title": "Project Diva", "text": "Divaparadises is a platform for AI-generated music videos."},
        {"title": "Gemini Model", "text": "Gemini 1.5 Pro has a 2 Million token context window."},
        {"title": "Embeddings", "text": "Embeddings are vector representations of text used for semantic search."},
        {"title": "Agentic AI", "text": "Agents can use tools to perform actions in the real world."}
    ]
    
    print(f"[INDEX] Embedding {len(knowledge_base)} documents...")
    # Extract texts for batch embedding
    texts = [doc["text"] for doc in knowledge_base]
    embeddings = embed_client.embed_batch(texts, task_type="retrieval_document")
    
    if not embeddings:
        print("[FAIL] Embeddings generation failed.")
        return

    # 2. User Query
    user_query = "What is the context window size of the Gemini model?"
    print(f"\n[USER]: {user_query}")
    
    # 3. Retrieve (Vector Search)
    query_vec = embed_client.embed_text(user_query, task_type="retrieval_query")
    
    # Calculate Scores
    scored_docs = []
    for i, doc_vec in enumerate(embeddings):
        score = cosine_similarity(query_vec, doc_vec)
        scored_docs.append((score, knowledge_base[i]))
        
    # Get Top match
    scored_docs.sort(key=lambda x: x[0], reverse=True)
    top_doc = scored_docs[0][1]
    print(f"[RETRIEVED]: {top_doc['title']} (Score: {scored_docs[0][0]:.4f})")
    
    # 4. Augment & Generate (RAG)
    rag_prompt = f"""
    Use the following Context to answer the Question.
    
    CONTEXT:
    {top_doc['text']}
    
    QUESTION:
    {user_query}
    """
    
    print("\n[GENERATING ANSWER]...")
    answer = text_client.generate_text(rag_prompt)
    print(f"\n[AI]: {answer}")

if __name__ == "__main__":
    main()
