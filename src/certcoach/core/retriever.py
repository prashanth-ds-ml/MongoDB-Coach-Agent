import os
import sys
import re
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
        or falls back to local Ollama if OpenRouter credentials are not configured.
        """
        openrouter_key = os.getenv("PREMIUM_API_KEY")
        
        # Build prompt for general LLM list-based reranking
        context_string = ""
        for idx, c in enumerate(chunks):
            context_string += f"\n--- Chunk {idx} ---\n{c['content']}\n"
            
        prompt = f"""
        You are an expert Reranker. Evaluate the following context chunks and determine which {top_n} are MOST relevant to the topic: "{topic}".
        Return only a JSON array of the best Chunk IDs (e.g. [0, 2, 4]).
        
        {context_string}
        """

        use_ollama = not openrouter_key or openrouter_key == "your_openrouter_key_here"
        content = ""

        if use_ollama:
            local_url = os.getenv("LOCAL_LLM_URL", "http://localhost:11434").rstrip("/")
            model_name = os.getenv("RERANK_MODEL") or os.getenv("MODEL", "qwen2.5-coder:7b")
            
            # Check if the user specified a dedicated local reranker model (like Qwen3-Reranker-4B)
            if "reranker" in model_name.lower():
                print(f"🚀 Running local Qwen-Reranker scoring loop using: '{model_name}'...")
                scored_chunks = []
                for chunk in chunks:
                    score_prompt = f"""
                    You are an expert relevance grader. Is the following document relevant to the user's query? Reply 'Yes' or 'No'.
                    Query: {topic}
                    Document: {chunk['content']}
                    """
                    payload = {
                        "model": model_name,
                        "messages": [{"role": "user", "content": score_prompt}],
                        "options": {"temperature": 0.0},
                        "stream": False
                    }
                    try:
                        response = requests.post(f"{local_url}/api/chat", json=payload, timeout=8)
                        if response.status_code == 200:
                            res_json = response.json()
                            ans = res_json.get("message", {}).get("content", "").strip().lower()
                            score = 1.0 if "yes" in ans else 0.0
                            scored_chunks.append((chunk, score))
                        else:
                            scored_chunks.append((chunk, 0.0))
                    except Exception:
                        scored_chunks.append((chunk, 0.0))
                # Sort by score descending
                scored_chunks.sort(key=lambda x: x[1], reverse=True)
                print("✅ Reranking via local cross-encoder complete.")
                return [sc[0] for sc in scored_chunks][:top_n]
            
            # General local chat model list-selection fallback
            print(f"🚀 OpenRouter key missing. Running local LLM Reranker using Ollama model: '{model_name}'...")
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "options": {"temperature": 0.1},
                "stream": False
            }
            try:
                response = requests.post(f"{local_url}/api/chat", json=payload, timeout=12)
                if response.status_code == 200:
                    res_json = response.json()
                    content = res_json.get("message", {}).get("content", "").strip()
                else:
                    print(f"⚠️ Local Ollama returned status {response.status_code}. Using defaults.")
                    return chunks[:top_n]
            except Exception as e:
                print(f"⚠️ Local Reranker failed: {e}. Using defaults.")
                return chunks[:top_n]
        else:
            print("🚀 Sending top chunks to OpenRouter for contextual reranking...")
            headers = {
                "Authorization": f"Bearer {openrouter_key}",
                "Content-Type": "application/json"
            }
            model_name = os.getenv("RERANK_MODEL", "google/gemma-2-9b-it:free")
            payload = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.1
            }
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload, timeout=10)
                if response.status_code == 200:
                    res_json = response.json()
                    content = res_json.get("choices", [{}])[0].get("message", {}).get("content", "").strip()
                else:
                    print(f"⚠️ OpenRouter returned status {response.status_code}. Using defaults.")
                    return chunks[:top_n]
            except Exception as e:
                print(f"⚠️ Reranker failed: {e}. Using defaults.")
                return chunks[:top_n]

        # Common Parsing Logic for General Chat Models
        try:
            match = re.search(r'\[\s*(\d+(?:\s*,\s*\d+)*)\s*\]', content)
            if match:
                indices = [int(i.strip()) for i in match.group(1).split(",")]
                reranked_chunks = []
                seen = set()
                for idx in indices:
                    if 0 <= idx < len(chunks) and idx not in seen:
                        reranked_chunks.append(chunks[idx])
                        seen.add(idx)
                # Append remaining chunks to preserve context
                for idx, chunk in enumerate(chunks):
                    if idx not in seen:
                        reranked_chunks.append(chunk)
                print(f"✅ Reranking successful. Ordered indices: {indices}")
                return reranked_chunks[:top_n]
            else:
                print(f"⚠️ Could not parse indices from rerank response. Raw content: {content[:150]}")
                return chunks[:top_n]
        except Exception as parse_err:
            print(f"⚠️ Rerank parsing failed: {parse_err}. Using defaults.")
            return chunks[:top_n]

if __name__ == "__main__":
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../chroma_db"))
    retriever = CertCoachRetriever(db_path)
    
    # Test query
    docs = retriever.retrieve_chunks("How does the MongoDB Aggregation Pipeline work?", k=5)
    final_docs = retriever.openrouter_rerank("MongoDB Aggregation Pipeline", docs, top_n=3)
    
    for idx, doc in enumerate(final_docs):
        print(f"\n[Rank {idx+1} | Source: {doc['source']}]\n{doc['content'][:200]}...\n")
