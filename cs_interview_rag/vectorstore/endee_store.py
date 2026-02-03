# Endee Vector Store - Integration with Endee vector database
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SearchResult:
    """Represents a search result from Endee."""
    id: str
    similarity: float
    content: str
    source: str
    metadata: Dict[str, Any]


class EndeeVectorStore:
    """
    Vector store implementation using Endee vector database.
    
    Endee is a high-performance vector database that provides:
    - Fast ANN (Approximate Nearest Neighbor) searches using HNSW algorithm
    - Support for cosine, L2, and inner product distance metrics
    - Metadata storage and filtering capabilities
    - Multiple quantization levels for speed/accuracy tradeoffs
    """
    
    def __init__(
        self,
        host: str = "http://localhost:8080",
        auth_token: Optional[str] = None,
        index_name: str = "cs_interview_docs",
        dimension: int = 384
    ):
        """
        Initialize the Endee vector store.
        
        Args:
            host: Endee server URL
            auth_token: Optional authentication token
            index_name: Name of the vector index
            dimension: Dimension of embedding vectors
        """
        try:
            from endee import Endee, Precision
        except ImportError:
            raise ImportError(
                "endee is required. Install with: pip install endee"
            )
        
        self.host = host
        self.auth_token = auth_token
        self.index_name = index_name
        self.dimension = dimension
        self.Precision = Precision
        
        # Initialize Endee client
        if auth_token:
            self.client = Endee(auth_token)
        else:
            self.client = Endee()
        
        # Set base URL
        self.client.set_base_url(f"{host}/api/v1")
        
        self._index = None
    
    def create_index(self, recreate: bool = False) -> None:
        """
        Create the vector index in Endee.
        
        Args:
            recreate: If True, delete existing index and create new one
        """
        # Check if index exists
        try:
            existing_indexes = self.client.list_indexes()
            # list_indexes() returns a list of index names (strings) or dicts
            if existing_indexes:
                if isinstance(existing_indexes[0], dict):
                    index_names = [idx.get("name") for idx in existing_indexes]
                else:
                    index_names = existing_indexes  # Already a list of strings
            else:
                index_names = []
            index_exists = self.index_name in index_names
        except Exception as e:
            print(f"Note: Could not list indexes ({e}), will try to create")
            index_exists = False
        
        if index_exists:
            if recreate:
                print(f"Deleting existing index: {self.index_name}")
                self.client.delete_index(name=self.index_name)
            else:
                print(f"Index '{self.index_name}' already exists")
                self._index = self.client.get_index(name=self.index_name)
                return
        
        # Create new index with cosine similarity and INT8D precision
        print(f"Creating index: {self.index_name} (dimension: {self.dimension})")
        self.client.create_index(
            name=self.index_name,
            dimension=self.dimension,
            space_type="cosine",
            precision=self.Precision.INT8D
        )
        
        self._index = self.client.get_index(name=self.index_name)
        print(f"Index '{self.index_name}' created successfully")
    
    def _get_index(self):
        """Get the index, creating if necessary."""
        if self._index is None:
            self._index = self.client.get_index(name=self.index_name)
        return self._index
    
    def upsert_chunks(
        self,
        chunks: List[Any],
        embeddings: List[List[float]]
    ) -> int:
        """
        Upsert chunks with their embeddings into Endee.
        
        Args:
            chunks: List of Chunk objects
            embeddings: List of embedding vectors
            
        Returns:
            Number of vectors upserted
        """
        if len(chunks) != len(embeddings):
            raise ValueError("Number of chunks and embeddings must match")
        
        if not chunks:
            return 0
        
        index = self._get_index()
        
        # Prepare vectors for upsert
        vectors = []
        for chunk, embedding in zip(chunks, embeddings):
            # Generate unique ID from source and chunk_id
            vector_id = f"{chunk.source}_chunk_{chunk.chunk_id}"
            
            # Create content preview (first 200 chars)
            content_preview = chunk.content[:200] + "..." if len(chunk.content) > 200 else chunk.content
            
            vectors.append({
                "id": vector_id,
                "vector": embedding,
                "meta": {
                    "source": chunk.source,
                    "chunk_id": chunk.chunk_id,
                    "content": chunk.content,
                    "content_preview": content_preview,
                    "start_char": chunk.start_char,
                    "end_char": chunk.end_char
                },
                "filter": {
                    "source": chunk.source
                }
            })
        
        # Upsert in batches of 100
        batch_size = 100
        total_upserted = 0
        
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            index.upsert(batch)
            total_upserted += len(batch)
            print(f"  Upserted {total_upserted}/{len(vectors)} vectors")
        
        return total_upserted
    
    def search(
        self,
        query_vector: List[float],
        top_k: int = 5,
        source_filter: Optional[str] = None
    ) -> List[SearchResult]:
        """
        Search for similar vectors in Endee.
        
        Args:
            query_vector: The query embedding vector
            top_k: Number of results to return
            source_filter: Optional filter by source document
            
        Returns:
            List of SearchResult objects
        """
        index = self._get_index()
        
        # Build query parameters
        query_params = {
            "vector": query_vector,
            "top_k": top_k,
            "ef": 128  # Higher ef for better recall
        }
        
        # Add filter if specified
        if source_filter:
            query_params["filter"] = [{"source": {"$eq": source_filter}}]
        
        # Execute search
        results = index.query(**query_params)
        
        # Convert to SearchResult objects
        search_results = []
        for item in results:
            meta = item.get("meta", {})
            search_results.append(SearchResult(
                id=item.get("id", ""),
                similarity=item.get("similarity", 0.0),
                content=meta.get("content", ""),
                source=meta.get("source", ""),
                metadata=meta
            ))
        
        return search_results
    
    def delete_index(self) -> None:
        """Delete the vector index."""
        try:
            self.client.delete_index(name=self.index_name)
            self._index = None
            print(f"Index '{self.index_name}' deleted")
        except Exception as e:
            print(f"Could not delete index: {e}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get index statistics."""
        try:
            index = self._get_index()
            info = index.describe()
            return info
        except Exception as e:
            return {"error": str(e)}
