# Document Loader - Load PDF, TXT, and Markdown files
import os
from pathlib import Path
from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Document:
    """Represents a loaded document."""
    content: str
    source: str
    metadata: Dict[str, Any]


class DocumentLoader:
    """Load documents from various file formats."""
    
    SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md", ".markdown"}
    
    def __init__(self):
        """Initialize the document loader."""
        pass
    
    def load_file(self, file_path: str) -> Document:
        """
        Load a single file based on its extension.
        
        Args:
            file_path: Path to the file
            
        Returns:
            Document object with content and metadata
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        extension = path.suffix.lower()
        
        if extension == ".pdf":
            content = self._load_pdf(path)
        elif extension in {".txt", ".md", ".markdown"}:
            content = self._load_text(path)
        else:
            raise ValueError(f"Unsupported file type: {extension}")
        
        return Document(
            content=content,
            source=path.name,
            metadata={
                "file_path": str(path.absolute()),
                "file_type": extension,
                "file_size": path.stat().st_size
            }
        )
    
    def _load_pdf(self, path: Path) -> str:
        """Extract text from a PDF file."""
        try:
            from pypdf import PdfReader
        except ImportError:
            raise ImportError("pypdf is required for PDF support. Install with: pip install pypdf")
        
        reader = PdfReader(str(path))
        text_parts = []
        
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        return "\n\n".join(text_parts)
    
    def _load_text(self, path: Path) -> str:
        """Load text from a plain text or markdown file."""
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    
    def load_directory(self, directory_path: str) -> List[Document]:
        """
        Load all supported documents from a directory.
        
        Args:
            directory_path: Path to the directory
            
        Returns:
            List of Document objects
        """
        path = Path(directory_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Directory not found: {directory_path}")
        
        if not path.is_dir():
            raise ValueError(f"Not a directory: {directory_path}")
        
        documents = []
        
        for file_path in path.rglob("*"):
            if file_path.is_file() and file_path.suffix.lower() in self.SUPPORTED_EXTENSIONS:
                try:
                    doc = self.load_file(str(file_path))
                    documents.append(doc)
                    print(f"  Loaded: {file_path.name}")
                except Exception as e:
                    print(f"  Warning: Could not load {file_path.name}: {e}")
        
        return documents
