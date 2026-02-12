"""
RAG (Retrieval Augmented Generation) Service using FAISS
"""
import os
import pickle
import faiss
import numpy as np
from typing import List, Tuple
from utils.embeddings import get_embeddings

FAISS_INDEX_PATH = "data/faiss_index/index.faiss"
CHUNKS_PATH = "data/faiss_index/chunks.pkl"

class RAGService:
    def __init__(self):
        self.index = None
        self.chunks = []
        self.dimension = 384  # all-MiniLM-L6-v2 dimension
        self.load_index()
    
    def create_index(self):
        """Create a new FAISS index"""
        os.makedirs("data/faiss_index", exist_ok=True)
        self.index = faiss.IndexFlatL2(self.dimension)
        self.chunks = []
        print("✅ Created new FAISS index")
        return self.index
    
    def load_index(self):
        """Load existing FAISS index or create new one if not exists"""
        os.makedirs("data/faiss_index", exist_ok=True)
        
        if os.path.exists(FAISS_INDEX_PATH) and os.path.exists(CHUNKS_PATH):
            # Load existing index
            self.index = faiss.read_index(FAISS_INDEX_PATH)
            with open(CHUNKS_PATH, 'rb') as f:
                self.chunks = pickle.load(f)
            print(f"✅ Loaded FAISS index with {len(self.chunks)} chunks")
        else:
            # Create new index
            self.create_index()
    
    def load_or_create_index(self):
        """Alias for load_index() - backward compatibility"""
        return self.load_index()
    
    def add_text_chunks(self, chunks: List[str], metadata: dict = None):
        """
        Add text chunks to FAISS index
        
        Args:
            chunks: List of text chunks
            metadata: Optional metadata (file_name, user_id, etc.)
        """
        if not chunks:
            return
        
        if metadata is None:
            metadata = {}
        
        # Generate embeddings for chunks
        embeddings = get_embeddings(chunks)
        
        # Add to FAISS index
        embeddings_array = np.array(embeddings).astype('float32')
        self.index.add(embeddings_array)
        
        # Store chunks with metadata
        for chunk in chunks:
            self.chunks.append({
                'text': chunk,
                'metadata': metadata
            })
        
        # Save index and chunks
        self.save_index()
        print(f"✅ Added {len(chunks)} chunks to FAISS index")
    
    def add_documents(self, text_chunks: List[str], metadata: dict):
        """
        Alias for add_text_chunks() - backward compatibility
        
        Args:
            text_chunks: List of text chunks
            metadata: Document metadata (file_name, user_id, etc.)
        """
        return self.add_text_chunks(text_chunks, metadata)
    
    def search_similar(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Search for similar chunks using vector similarity
        
        Args:
            query: Search query text
            top_k: Number of results to return (default: 3)
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = get_embeddings([query])[0]
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Search in FAISS
        distances, indices = self.index.search(query_vector, min(top_k, self.index.ntotal))
        
        # Get corresponding chunks
        results = []
        for idx, distance in zip(indices[0], distances[0]):
            if idx < len(self.chunks):
                results.append((self.chunks[idx]['text'], float(distance)))
        
        return results
    
    def retrieve(self, query: str, top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Alias for search_similar() - backward compatibility
        
        Args:
            query: User question
            top_k: Number of chunks to retrieve
            
        Returns:
            List of (chunk_text, similarity_score) tuples
        """
        return self.search_similar(query, top_k)
    
    def save_index(self):
        """Save FAISS index and chunks to disk"""
        faiss.write_index(self.index, FAISS_INDEX_PATH)
        with open(CHUNKS_PATH, 'wb') as f:
            pickle.dump(self.chunks, f)
    
    def get_context(self, query: str, top_k: int = 3) -> str:
        """
        Get formatted context from retrieved chunks
        """
        retrieved = self.retrieve(query, top_k)
        
        if not retrieved:
            return "No relevant context found in uploaded documents."
        
        context_parts = []
        for i, (chunk, score) in enumerate(retrieved, 1):
            context_parts.append(f"[Context {i}]\n{chunk}\n")
        
        return "\n".join(context_parts)

# Global RAG service instance
rag_service = RAGService()
