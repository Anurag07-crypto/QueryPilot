# ///////////////////////////////////////////////////
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
# ///////////////////////////////////////////////////
class Embedding_manager:
    def __init__(self, model_name:str="BAAI/bge-small-en-v1.5"):
        self.model_name = model_name
        self.model = None
        self._load_model()
    def _load_model(self):
        try:
            print(f"Embedding manager model {self.model_name} loaded")
            self.model = SentenceTransformer(
                model_name_or_path=self.model_name
            )
            print(f"Model Dimenstions are {self.model.get_sentence_embedding_dimension()}")
        except Exception as e:
            raise f"Embedding manager Model {self.model_name} is not loaded"
    def generate_embeddings(self,text:List[str])->np.ndarray:
        try:
            print("Genarating Embeddings")
            embeddings = self.model.encode(text)
            print(f"{len(embeddings)} Embeddings generated")
            return embeddings
        except Exception as e:
            print("Embeddings not generated")
            return None
