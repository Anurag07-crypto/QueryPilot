import chromadb
import uuid
from typing import List, Dict, Tuple, Any
import os
import numpy as np
from pathlib import Path
# //////////////////////////////////////////////
persistant_path = Path(__file__).parent.parent/ "data" / "vector_database"
# //////////////////////////////////////////////
class VectorStore:
    def __init__(self, collection_name:str="Text_Document",
                 persistent_directory=persistant_path):
        self.collection_name = collection_name
        self.persistent_directory = persistent_directory
        self.client = None
        self.collection = None
        self._initialize_store()
    def _initialize_store(self):
        try:
            os.makedirs(self.persistent_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persistent_directory)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description":"Text Document embedding for RAG"}
            )
            print(f"Vector Store Initialized {self.collection_name}")
            print(f"Existing Document in Collection {self.collection.count()}")
        except Exception as e:
            print(f"Vector Store Not Initialized: Error--->{e}")
    def add_documents(self, documents:List[Any], embeddings:np.ndarray):
        if len(documents) != len(embeddings):
            raise ValueError("Length of document and length of embeddings should be same")
        ids = []
        metadatas = []
        document_texts = []
        embedding_lists = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(id)
            metadata = dict(doc.metadata)
            metadata["doc_index"] = i
            metadata["content_length"] = len(doc.page_content)
            metadatas.append(metadata)
            document_texts.append(doc.page_content)
            embedding_lists.append(embedding.tolist())
        try:
            self.collection.add(
                ids=ids,
                embeddings=embedding_lists,
                metadatas=metadatas,
                documents=document_texts
            )
        except Exception as e:
            print("Error Raised", e)
            raise
        