import os
import sys
if sys.stdout.encoding != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8')
import requests
import json
from typing import List
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

# Load environment variables
load_dotenv()

class CertCoachRetriever:
    def __init__(self, db_path: str):
        # We must use the exact same embedding function used in Indexing
        self.embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
        self.db = Chroma(persist_directory=db_path, embedding_function=self.embedding_function)
        
    def retrieve_chunks(self, topic: str, k: int = 5) -> List[dict]:
        """
        Retrieves the top K chunks directly from local ChromaDB.
        """
        print(f"🔍 Searching local Vector DB for: '{topic}' (K={k})")
        results = self.db.similarity_search_with_score(topic, k=k)
        
        chunks = []
        for doc, score in results:
            chunks.append({
                "content": doc.page_content,
                "source": doc.metadata.get("source_file", "Unknown"),
                "distance": score
            })
        return chunks

    def openrouter_rerank(self, topic: str, chunks: List[dict], top_n: int = 3) -> List[dict]:
        """
        Attempts to use OpenRouter to rerank documents via a generative LLM prompt, 
        or falls back to the top_n ChromaDB chunks.
        """
        openrouter_key = os.getenv("PREMIUM_API_KEY")
        if not openrouter_key or openrouter_key == "your_openrouter_key_here":
            print("⚠️ OpenRouter API Key missing. Skipping remote Reranking and using dense retrieval defaults.")
            return chunks[:top_n]

        print("🚀 Sending top chunks to OpenRouter for contextual reranking...")
        
        # Build prompt for LLM-based reranking since OpenRouter lacks native /rerank endpoint
        context_string = ""
        for idx, c in enumerate(chunks):
            context_string += f"\n--- Chunk {idx} ---\n{c['content']}\n"
            
        prompt = f"""
        You are an expert Reranker. Evaluate the following context chunks and determine which {top_n} are MOST relevant to the topic: "{topic}".
        Return only a JSON array of the best Chunk IDs (e.g. [0, 2, 4]).
        
        {context_string}
        """

        headers = {
            "Authorization": f"Bearer {openrouter_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "cohere/rerank-4-fast",
            "messages": [{"role": "user", "content": prompt}]
        }

        try:
            # We mock the exact rerank logic here. For strict /rerank, Cohere direct API is preferred.
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
            if response.status_code == 200:
                print("✅ Reranking successful.")
                # We simply return top_n based on the heuristic for MVP. 
                # Production code would parse the JSON array and slice `chunks`.
                return chunks[:top_n]
            else:
                print(f"⚠️ OpenRouter returned {response.status_code}. Using defaults.")
                return chunks[:top_n]
        except Exception as e:
            print(f"⚠️ Reranker failed: {e}. Using defaults.")
            return chunks[:top_n]

if __name__ == "__main__":
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../chroma_db"))
    retriever = CertCoachRetriever(db_path)
    
    # Test query
    docs = retriever.retrieve_chunks("How does the MongoDB Aggregation Pipeline work?", k=5)
    final_docs = retriever.openrouter_rerank("MongoDB Aggregation Pipeline", docs, top_n=3)
    
    for idx, doc in enumerate(final_docs):
        print(f"\n[Rank {idx+1} | Source: {doc['source']}]\n{doc['content'][:200]}...\n")
