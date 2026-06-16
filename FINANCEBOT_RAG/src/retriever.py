import chromadb
from chromadb.utils import embedding_functions
from sentence_transformers import CrossEncoder
from typing import List, Dict

class Retriever:
    def __init__(self, db_path: str = "./chroma_db", collection_name: str = "gastos"):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="paraphrase-multilingual-MiniLM-L12-v2"
        )
        self.collection = self.client.get_collection(
            name=collection_name, 
            embedding_function=self.embedding_fn
        )
        # Cross-encoder for reranking (optional but requested)
        # Using a small multilingual cross-encoder
        self.reranker = CrossEncoder('cross-encoder/mmarco-mMiniLMv2-L12-H384-v1')

    def search(self, query: str, n_results: int = 5, use_reranking: bool = True):
        # Validate n_results against collection size (Problem 3)
        total_count = self.collection.count()
        n_results = min(n_results, total_count)
        
        if n_results == 0:
            return []

        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )

        # Chroma results structure: results['documents'][0], results['metadatas'][0], results['distances'][0]
        docs = results['documents'][0]
        metadatas = results['metadatas'][0]
        
        if not use_reranking or not docs:
            # Return top results directly if no reranking
            formatted_results = []
            for i in range(len(docs)):
                formatted_results.append({
                    "document": docs[i],
                    "metadata": metadatas[i],
                    "score": float(results['distances'][0][i])
                })
            # Sort distances (Chroma returns ascending distances - lower is better)
            # but for consistency with reranking we can just return what Chroma gave
            return self._normalize_scores(formatted_results[:3])

        # Reranking logic
        pairs = [[query, doc] for doc in docs]
        scores = self.reranker.predict(pairs)

        # Combine and sort by score (higher is better for cross-encoders)
        combined = []
        for i in range(len(docs)):
            combined.append({
                "document": docs[i],
                "metadata": metadatas[i],
                "score": float(scores[i])
            })
        
        # Sort by score descending
        reranked = sorted(combined, key=lambda x: x['score'], reverse=True)
        
        return self._normalize_scores(reranked[:3])

    def _normalize_scores(self, results: List[Dict]) -> List[Dict]:
        """
        Normalizes scores to a 0-1 range within the result set (Problem 1).
        """
        if not results:
            return []
            
        scores = [r["score"] for r in results]
        min_s, max_s = min(scores), max(scores)
        
        for r in results:
            if max_s == min_s:
                r["score_normalized"] = 1.0
            else:
                r["score_normalized"] = (r["score"] - min_s) / (max_s - min_s)
        
        return results

if __name__ == "__main__":
    retriever = Retriever()
    query = "Quanto gastei com combustível?"
    results = retriever.search(query)
    for res in results:
        print(f"Score: {res['score']:.4f} | {res['document']}")
