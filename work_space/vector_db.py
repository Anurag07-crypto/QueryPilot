import chromadb
import uuid
from typing import List, Any
import os
import numpy as np
from pathlib import Path
from .logger import get_logger

logger = get_logger(__name__)
persistent_path = Path(__file__).parent.parent/ "data" / "vector_database"

class VectorStore:
    """Manages ChromaDB persistent vector storage for RAG pipeline."""
    
    def __init__(self, collection_name:str="Text_Document",
                 persistent_directory=persistent_path):
        self.collection_name = collection_name
        self.persistent_directory = persistent_directory
        self.client = None
        self.collection = None
        self._initialize_store()
        
    def _initialize_store(self):
        """Initialize ChromaDB client and collection.
        Raises:
            RuntimeError: If ChromaDB fails to initialize
        """
        
        try:
            os.makedirs(self.persistent_directory, exist_ok=True)
            self.client = chromadb.PersistentClient(path=self.persistent_directory)
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description":"Text Document embedding for RAG"}
            )
            
            logger.info(f"Vector Store Initialized {self.collection_name}")
            logger.debug(f"Existing Document in Collection {self.collection.count()}")
        
        except Exception as e:
            logger.critical(f"Vector store not Initialized: {e}")
            raise RuntimeError(f"Vector Store Not Initialized: {e}") from e
    
    def add_documents(self, documents:List[Any], embeddings:np.ndarray):
        """Add documents and embeddings to ChromaDB collection.

        Args:
            documents: List of LangChain document objects
            embeddings: Numpy array of embedding vectors

        Raises:
            ValueError: If document and embedding counts don't match
            RuntimeError: If ChromaDB insertion fails
        """
        
        if len(documents) != len(embeddings):
            raise ValueError("Length of document and length of embeddings should be same")
        ids = []
        metadatas = []
        document_texts = []
        embedding_lists = []
        for i, (doc, embedding) in enumerate(zip(documents, embeddings)):
            doc_id = f"doc_{uuid.uuid4().hex[:8]}_{i}"
            ids.append(doc_id)
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
            
            logger.info(f"{len(ids)} documents added to ChromaDB")
       
        except Exception as e:
            logger.error(f"Failed to add documents to ChromaDB: {e}",
                         exc_info=True)
            raise RuntimeError(f"Failed to add documents to ChromaDB: {e}") from e 
        
