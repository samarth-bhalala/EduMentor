"""
Embedding generation using sentence-transformers
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np

# Load model once (global)
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts: List[str]) -> List[np.ndarray]:
    """
    Generate embeddings for a list of texts
    
    Args:
        texts: List of text strings
        
    Returns:
        List of embedding vectors
    """
    embeddings = model.encode(texts, show_progress_bar=False)
    return embeddings.tolist()

def get_single_embedding(text: str) -> np.ndarray:
    """
    Generate embedding for a single text
    
    Args:
        text: Input text
        
    Returns:
        Embedding vector
    """
    return model.encode([text], show_progress_bar=False)[0]
