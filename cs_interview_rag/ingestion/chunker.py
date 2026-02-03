# Text Chunker - Split documents into overlapping chunks
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Chunk:
    """Represents a text chunk with metadata."""
    content: str
    chunk_id: int
    source: str
    start_char: int
    end_char: int
    metadata: Dict[str, Any]


class TextChunker:
    """Split text into overlapping chunks for embedding."""
    
    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        """
        Initialize the text chunker.
        
        Args:
            chunk_size: Maximum characters per chunk
            chunk_overlap: Number of overlapping characters between chunks
        """
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap must be less than chunk_size")
        
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def chunk_text(self, text: str, source: str = "unknown") -> List[Chunk]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: The text to split
            source: Source identifier for metadata
            
        Returns:
            List of Chunk objects
        """
        if not text or not text.strip():
            return []
        
        # Clean up the text
        text = text.strip()
        
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            # Calculate end position
            end = min(start + self.chunk_size, len(text))
            
            # Try to break at a sentence or paragraph boundary
            if end < len(text):
                # Look for sentence boundaries (., !, ?) followed by space or newline
                best_break = end
                for break_char in ["\n\n", "\n", ". ", "! ", "? ", ", "]:
                    last_break = text.rfind(break_char, start, end)
                    if last_break > start + self.chunk_size // 2:
                        best_break = last_break + len(break_char)
                        break
                end = best_break
            
            # Extract chunk content
            chunk_content = text[start:end].strip()
            
            if chunk_content:
                chunks.append(Chunk(
                    content=chunk_content,
                    chunk_id=chunk_id,
                    source=source,
                    start_char=start,
                    end_char=end,
                    metadata={
                        "chunk_size": len(chunk_content),
                        "total_chunks": -1  # Will be updated after processing
                    }
                ))
                chunk_id += 1
            
            # Move start position with overlap
            start = end - self.chunk_overlap
            if start >= len(text) or start == end - self.chunk_overlap and end == len(text):
                break
        
        # Update total chunks count
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)
        
        return chunks
    
    def chunk_documents(self, documents) -> List[Chunk]:
        """
        Chunk multiple documents.
        
        Args:
            documents: List of Document objects
            
        Returns:
            List of all Chunk objects
        """
        all_chunks = []
        
        for doc in documents:
            chunks = self.chunk_text(doc.content, doc.source)
            all_chunks.extend(chunks)
        
        return all_chunks
