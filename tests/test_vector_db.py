import pytest
import numpy as np 
from unittest.mock import MagicMock, patch
from work_space.vector_db import VectorStore


class TestVectorStore:
    """Tests for VectorStore class."""
    def test_mismatched_documents_embeddings_raises_error(self):
        """Should raise ValueError if counts don't match."""
        # Mock the entire ChromaDb initialization
        with patch("work_space.vector_db.chromadb.PersistentClient"):
            store = VectorStore()
        
        # 2 documents but 3 embeddings - should raise 
        mock_docs = [MagicMock(), MagicMock()]
        mock_embeddings = np.random.rand(3, 384)
        
        with pytest.raises(ValueError):
            store.add_documents(mock_docs, mock_embeddings)
        
    def test_add_documents_call_collection(self):
        """ChromaDB collection.add() should be called once."""
        with patch("work_space.vector_db.chromadb.PersistentClient"):
            store = VectorStore()
        
        store.collection = MagicMock()
        
        mock_docs = [MagicMock(
            page_content="test content",
            metadata={"source":"test.txt"}
        )]
        mock_embeddings = np.random.rand(1,384)
        
        store.add_documents(mock_docs, mock_embeddings)
        
        # verify collection.add was called
        store.collection.add.assert_called_once()
        
    def test_initialization_failure_raises_runtime_error(self):
        """If ChromaDB fails to init, should raise RuntimeError."""
        with patch(
            "work_space.vector_db.chromadb.PersistentClient",
            side_effect=Exception("DB connection failed")
        ):
            with pytest.raises(RuntimeError):
                VectorStore()