# Embedder - Generate embeddings using sentence-transformers
from typing import List, Union
import numpy as np


class Embedder:
    """Generate embeddings using sentence-transformers."""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        """
        Initialize the embedder with a sentence-transformer model.
        
        Args:
            model_name: Name of the sentence-transformer model
        """
        try:
            from sentence_transformers import SentenceTransformer
        except ImportError:
            raise ImportError(
                "sentence-transformers is required. "
                "Install with: pip install sentence-transformers"
            )
        
        self.model_name = model_name
        self.model = SentenceTransformer(model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()
        print(f"Loaded embedding model: {model_name} (dimension: {self.dimension})")
    
    def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.
        
        Args:
            text: Text to embed
            
        Returns:
            Embedding as a list of floats
        """
        if not text or not text.strip():
            raise ValueError("Cannot embed empty text")
        
        embedding = self.model.encode(text, convert_to_numpy=True)
        return embedding.tolist()
    
    def embed_batch(self, texts: List[str], batch_size: int = 32) -> List[List[float]]:
        """
        Generate embeddings for multiple texts.
        
        Args:
            texts: List of texts to embed
            batch_size: Number of texts to process at once
            
        Returns:
            List of embeddings, each as a list of floats
        """
        if not texts:
            return []
        
        # Filter empty texts but track indices
        valid_texts = []
        valid_indices = []
        for i, text in enumerate(texts):
            if text and text.strip():
                valid_texts.append(text)
                valid_indices.append(i)
        
        if not valid_texts:
            return [[] for _ in texts]
        
        # Generate embeddings
        embeddings = self.model.encode(
            valid_texts,
            batch_size=batch_size,
            show_progress_bar=len(valid_texts) > 10,
            convert_to_numpy=True
        )
        
        # Map back to original indices
        result = [[] for _ in texts]
        for i, idx in enumerate(valid_indices):
            result[idx] = embeddings[i].tolist()
        
        return result
    
    def get_dimension(self) -> int:
        """Get the embedding dimension."""
        return self.dimension
