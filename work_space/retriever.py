from .vector_db import VectorStore
from .embedding_manager import EmbeddingManager
from typing import List, Any, Dict

class Retriever:
    def __init__(self, embedding_manager:EmbeddingManager, vector_store:VectorStore):
        self.embedding_manager = embedding_manager
        self.vector_store = vector_store
    def retrieve(self, query:str, top_k:int=5, threshold:float = 0.2) -> List[Dict[str, Any]]:
        try:
            query_embedding = self.embedding_manager.generate_embeddings([query])[0]
            results = self.vector_store.collection.query(
                query_embeddings=[query_embedding.tolist()],
                n_results=top_k,
                include = ["metadatas", "documents", "distances"]
            )
            
            retrieved_docs = []
            
            if results["documents"] and results["documents"][0]:
                documents = results["documents"][0]
                metadatas = results["metadatas"][0]
                distances = results["distances"][0]
                ids = results["ids"][0]
                
                for i, (doc_id, document, metadata, distance) in enumerate(
                    zip(ids, documents, metadatas, distances)
                ):
                    similarity_score = 1 - distance

                    if similarity_score < threshold:
                        continue

                    retrieved_docs.append(
                        {
                            "id": doc_id,
                            "content": document,
                            "metadata": metadata,
                            "similarity_score": similarity_score,
                            "distance": distance,
                            "rank": i + 1,
                        }
                    )

            if not retrieved_docs:
                print("No documents found")

            print(
                f"Retrieved {len(retrieved_docs)} documents"
            )
            return retrieved_docs

        except Exception as e:
            print(f"Error during retrieval: {e}")
            return []
