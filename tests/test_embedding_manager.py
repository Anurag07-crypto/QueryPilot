import numpy as np 
import pytest
from work_space.embedding_manager import EmbeddingManager

class TestEmbeddingManager:
    """Test For EmbeddingManager Class."""
    
    def setup_method(self):
        """Runs before every test - creates fresh manager."""
        self.manager = EmbeddingManager()
    
    def test_model_loads_successfully(self):
        """Model should load without errors."""
        assert self.manager.model is not None
    
    def test_embeddings_correct_count(self):
        """Should return one embedding per input text."""
        texts = ["hello world", "pytest is great"]
        result = self.manager.generate_embeddings(texts)
        assert result.shape[0] == 2
        
    def test_embeddings_return_numpy_array(self):
        """Output should always be a numpy array."""
        result = self.manager.generate_embeddings(["test"])
        assert isinstance(result, np.ndarray)
        
    def test_empty_input_returns_empty_array(self):
        """Empty list should return empty array, not crash."""
        result = self.manager.generate_embeddings([])
        assert len(result) == 0
        
    def test_embeddings_have_correct_dimensions(self):
        """BGE-small produces 384-dimesional embeddings."""
        result = self.manager.generate_embeddings(["tests"])
        assert result.shape[1] == 384
        
    def test_invalid_model_raises_runtime_error(self):
        """Bad model name should raise a RuntimeError, not crash."""
        with pytest.raises(RuntimeError):
            EmbeddingManager(model_name="ANUU/nonexistant-model")