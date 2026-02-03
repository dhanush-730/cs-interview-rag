# RAG Pipeline - Retrieval-Augmented Generation for CS Interview Prep
from typing import List, Optional, Dict, Any
from dataclasses import dataclass

from ingestion import DocumentLoader, TextChunker
from embeddings import Embedder
from vectorstore import EndeeVectorStore


@dataclass
class RAGResponse:
    """Response from the RAG pipeline."""
    answer: str
    sources: List[Dict[str, Any]]
    query: str
    retrieved_chunks: int


# System prompt that enforces strict grounding
SYSTEM_PROMPT = """You are a Computer Science interview preparation assistant. Your role is to help candidates understand CS concepts for technical interviews.

CRITICAL RULES:
1. Answer ONLY using the provided context below
2. If the context doesn't contain relevant information, say: "I don't have information about this topic in my current knowledge base. Please add relevant study materials."
3. Never make up information or use knowledge outside the provided context
4. Cite the source document when providing information
5. Keep answers concise but comprehensive enough for interview preparation

Context from study materials:
{context}

---
Answer the following question based ONLY on the context above."""


class RAGPipeline:
    """
    RAG (Retrieval-Augmented Generation) Pipeline for CS Interview Prep.
    
    This pipeline:
    1. Ingests documents (PDF/TXT/MD) and chunks them
    2. Generates embeddings using sentence-transformers
    3. Stores vectors in Endee vector database
    4. Retrieves relevant chunks for user queries
    5. Generates grounded answers using an LLM
    """
    
    def __init__(
        self,
        embedder: Embedder,
        vector_store: EndeeVectorStore,
        llm_api_key: Optional[str] = None,
        llm_model: str = "gemini-2.0-flash",
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
        top_k: int = 5
    ):
        """
        Initialize the RAG pipeline.
        
        Args:
            embedder: Embedder instance for generating embeddings
            vector_store: EndeeVectorStore instance for vector storage
            llm_api_key: Google API key for Gemini
            llm_model: LLM model to use
            chunk_size: Characters per chunk
            chunk_overlap: Overlap between chunks
            top_k: Number of chunks to retrieve
        """
        self.embedder = embedder
        self.vector_store = vector_store
        self.llm_api_key = llm_api_key
        self.llm_model = llm_model
        self.top_k = top_k
        
        self.document_loader = DocumentLoader()
        self.chunker = TextChunker(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        
        # Initialize LLM client
        self._llm_client = None
        self._llm_type = None  # 'ollama' or 'gemini'
        self._init_llm()
    
    def _init_llm(self):
        """Initialize the LLM client. Tries Ollama first (local), then Gemini."""
        # Try Ollama first (local, no rate limits)
        try:
            import requests
            # Check if Ollama is running
            response = requests.get("http://localhost:11434/api/tags", timeout=2)
            if response.status_code == 200:
                self._llm_type = 'ollama'
                print(f"LLM initialized: Ollama ({self.llm_model})")
                return
        except:
            pass  # Ollama not available, try Gemini
        
        # Try Gemini if API key provided
        if self.llm_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.llm_api_key)
                self._llm_client = genai.GenerativeModel(self.llm_model)
                self._llm_type = 'gemini'
                print(f"LLM initialized: Gemini ({self.llm_model})")
                return
            except ImportError:
                print("Warning: google-generativeai not installed.")
            except Exception as e:
                print(f"Warning: Could not initialize Gemini: {e}")
        
        print("No LLM available. Install Ollama or configure GOOGLE_API_KEY.")
    
    def ingest_documents(self, directory: str, recreate_index: bool = False) -> int:
        """
        Ingest documents from a directory into Endee.
        
        Args:
            directory: Path to directory containing documents
            recreate_index: If True, delete and recreate the index
            
        Returns:
            Number of chunks ingested
        """
        print(f"\n{'='*50}")
        print("DOCUMENT INGESTION PIPELINE")
        print(f"{'='*50}")
        
        # Step 1: Load documents
        print(f"\n[1/4] Loading documents from: {directory}")
        documents = self.document_loader.load_directory(directory)
        print(f"      Loaded {len(documents)} documents")
        
        if not documents:
            print("No documents found!")
            return 0
        
        # Step 2: Chunk documents
        print(f"\n[2/4] Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)
        print(f"      Created {len(chunks)} chunks")
        
        # Step 3: Generate embeddings
        print(f"\n[3/4] Generating embeddings...")
        texts = [chunk.content for chunk in chunks]
        embeddings = self.embedder.embed_batch(texts)
        print(f"      Generated {len(embeddings)} embeddings")
        
        # Step 4: Store in Endee
        print(f"\n[4/4] Storing in Endee vector database...")
        self.vector_store.create_index(recreate=recreate_index)
        num_stored = self.vector_store.upsert_chunks(chunks, embeddings)
        
        print(f"\n{'='*50}")
        print(f"INGESTION COMPLETE: {num_stored} chunks stored in Endee")
        print(f"{'='*50}\n")
        
        return num_stored
    
    def query(self, question: str, top_k: Optional[int] = None) -> RAGResponse:
        """
        Query the RAG system with a question.
        
        Args:
            question: The user's question
            top_k: Number of chunks to retrieve (overrides default)
            
        Returns:
            RAGResponse with answer and sources
        """
        k = top_k or self.top_k
        
        print(f"\n{'='*50}")
        print("RAG QUERY PIPELINE")
        print(f"{'='*50}")
        print(f"Question: {question}")
        
        # Step 1: Embed the query
        print(f"\n[1/3] Embedding query...")
        query_embedding = self.embedder.embed_text(question)
        
        # Step 2: Search Endee for similar chunks
        print(f"[2/3] Searching Endee (top_k={k})...")
        search_results = self.vector_store.search(query_embedding, top_k=k)
        print(f"      Found {len(search_results)} relevant chunks")
        
        if not search_results:
            return RAGResponse(
                answer="I couldn't find any relevant information in my knowledge base. Please make sure documents have been ingested.",
                sources=[],
                query=question,
                retrieved_chunks=0
            )
        
        # Build context from retrieved chunks
        context_parts = []
        sources = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(f"[{i}] From '{result.source}' (similarity: {result.similarity:.3f}):\n{result.content}")
            sources.append({
                "source": result.source,
                "similarity": result.similarity,
                "preview": result.content[:150] + "..." if len(result.content) > 150 else result.content
            })
        
        context = "\n\n---\n\n".join(context_parts)
        
        # Step 3: Generate answer using LLM
        print(f"[3/3] Generating answer with LLM...")
        
        if self._llm_type is None:
            # No LLM available, return retrieved context
            answer = f"Retrieved context (LLM not configured):\n\n{context}"
        else:
            try:
                # Build prompt with context
                prompt = SYSTEM_PROMPT.format(context=context)
                full_prompt = f"{prompt}\n\nQuestion: {question}\n\nAnswer:"
                
                if self._llm_type == 'ollama':
                    # Use Ollama API
                    import requests
                    response = requests.post(
                        "http://localhost:11434/api/generate",
                        json={
                            "model": self.llm_model,
                            "prompt": full_prompt,
                            "stream": False
                        },
                        timeout=180  # Increased for first-time model loading
                    )
                    answer = response.json().get("response", "No response from Ollama")
                else:
                    # Use Gemini
                    response = self._llm_client.generate_content(full_prompt)
                    answer = response.text
            except Exception as e:
                answer = f"Error generating answer: {e}\n\nRetrieved context:\n{context}"
        
        print(f"\n{'='*50}")
        print("ANSWER:")
        print(f"{'='*50}")
        print(answer)
        print(f"\nSources: {[s['source'] for s in sources]}")
        print(f"{'='*50}\n")
        
        return RAGResponse(
            answer=answer,
            sources=sources,
            query=question,
            retrieved_chunks=len(search_results)
        )
    
    def clear_index(self) -> None:
        """Clear the vector index."""
        self.vector_store.delete_index()
        print("Index cleared.")
