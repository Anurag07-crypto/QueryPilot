
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from .logger import get_logger

logger = get_logger(__name__)

class EmbeddingManager:
    """Manages sentence embedding generation using SentenceTransformer."""
    
    def __init__(self, model_name:str="BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    def _load_model(self):
        """Load the SentenceTransformer Model from HuggingFace or local cache
        Raises:
            RuntimeError: If model is not found or fails to load
        """
        
        try:
            self.model = SentenceTransformer(
                model_name_or_path=self.model_name
            )
            
            logger.info(f"Model Loaded: {self.model_name}")
            logger.debug(
                f"Model Dimensions: " 
                f"{self.model.get_sentence_embedding_dimension()}"
                )
            
        except OSError as e:
            # model file not found or corrupted
            logger.critical(f"Model file not found: {self.model_name}")
            raise RuntimeError(f"Model file not found: {self.model_name}") from e
        
        except Exception as e:
            # anything unexpected
            logger.critical(f"Unexpected error loading model: {e}")
            raise RuntimeError(f"Unexpected error loading :{e}") from e
    
    def generate_embeddings(self,text:List[str])->np.ndarray:
        """Generate embeddings for a list of text strings.
        Args:
            texts: List of strings to embed
        
        Returns:
            Numpy array of embeddings, empty array if input is empty
            
        Raises:
            RuntimeError: If embedding generation fails        
        """
        
        if not text:
            logger.warning("Empty text list passed to generate_embeddings")
            return np.array([])
        
        try:
            logger.debug("Generating Embeddings")
            embeddings = self.model.encode(text)
            logger.info(f"{len(embeddings)} Embeddings generated")
            return embeddings
        
        except Exception as e:
            logger.error(f"Embedding not generated: {e}")
            raise RuntimeError(f"Embeddings not generated {e}") from e

