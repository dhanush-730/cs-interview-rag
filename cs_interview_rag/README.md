# CS Interview RAG Assistant

A production-ready **Retrieval-Augmented Generation (RAG)** system for Computer Science interview preparation, powered by **Endee** vector database.

## 🎯 Problem Statement

Candidates preparing for technical interviews struggle to revise large volumes of CS theory (DSA, OS, DBMS, OOP). Traditional keyword search fails when users phrase questions differently. This RAG system retrieves relevant study material based on **semantic meaning** and generates **grounded answers** using retrieved context only.

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        INGESTION PIPELINE                                │
├─────────────────────────────────────────────────────────────────────────┤
│  Documents     →    Document      →    Chunker     →    Embedder        │
│  (PDF/TXT/MD)       Loader              (1000 chars)    (MiniLM-384)    │
│                                                               │         │
│                                                               ▼         │
│                                                 ┌─────────────────────┐ │
│                                                 │   ENDEE VECTOR DB   │ │
│                                                 │  • Cosine similarity│ │
│                                                 │  • HNSW index       │ │
│                                                 │  • Metadata storage │ │
│                                                 └─────────────────────┘ │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                         QUERY PIPELINE                                   │
├─────────────────────────────────────────────────────────────────────────┤
│  User Query  →  Query Embedding  →  Endee Search  →  Retrieved Chunks   │
│                     (MiniLM)           (top-k)           │              │
│                                                          ▼              │
│                                                   ┌────────────────┐    │
│                                                   │  LLM (Gemini)  │    │
│                                                   │  With strict   │    │
│                                                   │  grounding     │    │
│                                                   └───────┬────────┘    │
│                                                           ▼             │
│                                                   Grounded Answer       │
│                                                   + Source Citations    │
└─────────────────────────────────────────────────────────────────────────┘
```

## 🔑 Endee Vector Database: The Core

**Endee** is a high-performance vector database that serves as the backbone of this RAG system.

### Why Endee?

| Feature | Benefit |
|---------|---------|
| **HNSW Algorithm** | Fast approximate nearest neighbor search |
| **Cosine Similarity** | Optimal for semantic text embeddings |
| **Metadata Storage** | Store source, chunk_id, content with vectors |
| **Filtering** | Query specific documents using filters |
| **INT8D Quantization** | Balance between speed and accuracy |

### How Endee is Used

1. **Index Creation**: Create a vector index with 384 dimensions (matching MiniLM embeddings)
2. **Vector Upsert**: Store document chunks with:
   - Unique ID: `{source}_chunk_{id}`
   - Vector: 384-dimensional embedding
   - Metadata: source file, chunk content, position
   - Filter: source document for targeted search
3. **Similarity Search**: Query with embedded question to find top-k relevant chunks
4. **Grounded Response**: Retrieved chunks feed the LLM for contextual answers

## 📁 Project Structure

```
cs_interview_rag/
├── config/
│   ├── __init__.py
│   └── settings.py          # Environment-based configuration
├── ingestion/
│   ├── __init__.py
│   ├── document_loader.py   # PDF/TXT/MD file loader
│   └── chunker.py           # Intelligent text chunking
├── embeddings/
│   ├── __init__.py
│   └── embedder.py          # Sentence transformer embeddings
├── vectorstore/
│   ├── __init__.py
│   └── endee_store.py       # Endee vector database integration
├── rag/
│   ├── __init__.py
│   └── pipeline.py          # Complete RAG pipeline
├── data/
│   └── sample_materials/    # Sample CS study materials
│       ├── dsa_basics.md
│       ├── oop_concepts.md
│       └── os_fundamentals.md
├── main.py                  # CLI entry point
├── requirements.txt
├── .env.example
└── README.md
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8+
- Docker (for Endee server)
- Google API key (for Gemini LLM)

### 2. Start Endee Server

```bash
docker run -d -p 8080:8080 --name endee-server endeeio/endee-server:latest
```

Verify it's running:
```bash
curl http://localhost:8080/health
```

### 3. Install Dependencies

```bash
cd cs_interview_rag
pip install -r requirements.txt
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

### 5. Ingest Study Materials

```bash
python main.py ingest ./data/sample_materials
```

Expected output:
```
==================================================
DOCUMENT INGESTION PIPELINE
==================================================

[1/4] Loading documents from: ./data/sample_materials
      Loaded 3 documents

[2/4] Chunking documents...
      Created 25 chunks

[3/4] Generating embeddings...
      Generated 25 embeddings

[4/4] Storing in Endee vector database...
Creating index: cs_interview_docs (dimension: 384)
      Upserted 25/25 vectors

==================================================
INGESTION COMPLETE: 25 chunks stored in Endee
==================================================
```

### 6. Ask Questions

```bash
# Single question
python main.py query "What is a binary search tree?"

# Interactive mode
python main.py interactive
```

## 📖 CLI Commands

| Command | Description |
|---------|-------------|
| `python main.py ingest <dir>` | Ingest documents from directory |
| `python main.py query "<question>"` | Ask a single question |
| `python main.py interactive` | Start interactive Q&A session |
| `python main.py status` | Show Endee index status |
| `python main.py clear` | Delete all indexed documents |

### Examples

```bash
# Ingest documents (recreate index)
python main.py ingest ./data/sample_materials --recreate

# Ask about data structures
python main.py query "Explain the difference between a stack and a queue"

# Ask about algorithms
python main.py query "What is the time complexity of quicksort?"

# Ask about OOP
python main.py query "What are the four pillars of OOP?"

# Ask about OS
python main.py query "What is a deadlock and how to prevent it?"
```

## ⚙️ Configuration

All settings are configurable via environment variables or `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `ENDEE_HOST` | `http://localhost:8080` | Endee server URL |
| `ENDEE_AUTH_TOKEN` | (none) | Optional auth token |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | Sentence transformer model |
| `CHUNK_SIZE` | `1000` | Characters per chunk |
| `CHUNK_OVERLAP` | `200` | Overlap between chunks |
| `TOP_K` | `5` | Chunks to retrieve per query |
| `GOOGLE_API_KEY` | (required) | Google API key for Gemini |

## 🔒 Strict Grounding

The system enforces **strict grounding** - the LLM can ONLY answer using retrieved context:

```python
SYSTEM_PROMPT = """
Answer ONLY using the provided context.
If the context doesn't contain relevant information, say: 
"I don't have information about this topic in my current knowledge base."
"""
```

This ensures:
- ✅ No hallucination
- ✅ Answers based on your study materials
- ✅ Source citations for verification

## 📚 Adding Your Own Materials

1. Add PDF, TXT, or MD files to a directory
2. Run ingestion:
   ```bash
   python main.py ingest /path/to/your/materials
   ```
3. The system will automatically:
   - Load all supported file types
   - Chunk them intelligently
   - Generate embeddings
   - Store in Endee

## 🧪 How Vector Search Works

1. **Your Question**: "What is polymorphism?"
2. **Embedding**: Convert to 384-dimensional vector
3. **Endee Search**: Find top-5 similar chunks using cosine similarity
4. **Retrieved**: Chunks about OOP polymorphism from study materials
5. **LLM Response**: Generate answer grounded in retrieved context

## 📄 License

MIT License

## 🙏 Acknowledgments

- **Endee** - High-performance vector database
- **Sentence Transformers** - Text embeddings
- **Google Gemini** - LLM for response generation
