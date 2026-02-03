#!/usr/bin/env python3
"""
CS Interview RAG Assistant - Command Line Interface

A RAG-based AI assistant for Computer Science interview preparation.
Uses Endee vector database for semantic search and LLM for grounded answers.

Usage:
    python main.py ingest <directory>     - Ingest documents from directory
    python main.py query "<question>"     - Ask a question
    python main.py interactive            - Interactive Q&A mode
    python main.py clear                  - Clear the vector index
    python main.py status                 - Show index status
"""

import argparse
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import settings
from embeddings import Embedder
from vectorstore import EndeeVectorStore
from rag import RAGPipeline


def create_pipeline() -> RAGPipeline:
    """Create and configure the RAG pipeline."""
    # Initialize embedder
    embedder = Embedder(model_name=settings.embedding_model)
    
    # Initialize Endee vector store
    vector_store = EndeeVectorStore(
        host=settings.endee_host,
        auth_token=settings.endee_auth_token,
        index_name=settings.endee_index_name,
        dimension=settings.embedding_dimension
    )
    
    # Create RAG pipeline
    pipeline = RAGPipeline(
        embedder=embedder,
        vector_store=vector_store,
        llm_api_key=settings.google_api_key,
        llm_model=settings.llm_model,
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        top_k=settings.top_k
    )
    
    return pipeline


def cmd_ingest(args):
    """Ingest documents from a directory."""
    if not os.path.exists(args.directory):
        print(f"Error: Directory not found: {args.directory}")
        return 1
    
    pipeline = create_pipeline()
    num_chunks = pipeline.ingest_documents(
        args.directory,
        recreate_index=args.recreate
    )
    
    if num_chunks > 0:
        print(f"\nSuccess! Ingested {num_chunks} chunks into Endee.")
    return 0


def cmd_query(args):
    """Query the RAG system."""
    if not args.question:
        print("Error: Please provide a question")
        return 1
    
    pipeline = create_pipeline()
    response = pipeline.query(args.question, top_k=args.top_k)
    
    # Pretty print the answer
    print("\n" + "="*60)
    print("ANSWER")
    print("="*60)
    print(response.answer)
    print("\n" + "-"*60)
    print(f"Sources ({len(response.sources)} chunks retrieved):")
    for i, src in enumerate(response.sources, 1):
        print(f"  [{i}] {src['source']} (similarity: {src['similarity']:.3f})")
    print("="*60 + "\n")
    
    return 0


def cmd_interactive(args):
    """Interactive Q&A mode."""
    print("\n" + "="*60)
    print("CS INTERVIEW PREP - INTERACTIVE MODE")
    print("="*60)
    print("Ask questions about Computer Science topics.")
    print("Type 'exit' or 'quit' to end the session.")
    print("Type 'help' for available commands.")
    print("="*60 + "\n")
    
    pipeline = create_pipeline()
    
    while True:
        try:
            question = input("\n📚 Your question: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\nGoodbye! Good luck with your interviews! 🎯")
                break
            
            if question.lower() == 'help':
                print("\nCommands:")
                print("  exit/quit/q - Exit interactive mode")
                print("  help        - Show this help message")
                print("  clear       - Clear the screen")
                print("\nOr just type your CS question!")
                continue
            
            if question.lower() == 'clear':
                os.system('cls' if os.name == 'nt' else 'clear')
                continue
            
            # Query the RAG system
            response = pipeline.query(question)
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
    
    return 0


def cmd_clear(args):
    """Clear the vector index."""
    confirm = input("Are you sure you want to clear all indexed documents? (yes/no): ")
    if confirm.lower() != 'yes':
        print("Cancelled.")
        return 0
    
    pipeline = create_pipeline()
    pipeline.clear_index()
    print("Index cleared.")
    return 0


def cmd_status(args):
    """Show index status."""
    pipeline = create_pipeline()
    stats = pipeline.vector_store.get_stats()
    
    print("\n" + "="*40)
    print("ENDEE INDEX STATUS")
    print("="*40)
    print(f"Host: {settings.endee_host}")
    print(f"Index: {settings.endee_index_name}")
    print(f"Stats: {stats}")
    print("="*40 + "\n")
    
    return 0


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="CS Interview RAG Assistant - Powered by Endee Vector Database",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest documents from a directory')
    ingest_parser.add_argument('directory', help='Path to directory containing documents')
    ingest_parser.add_argument('--recreate', action='store_true', 
                               help='Delete and recreate the index')
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Ask a question')
    query_parser.add_argument('question', help='Your CS interview question')
    query_parser.add_argument('--top-k', type=int, default=5,
                              help='Number of chunks to retrieve (default: 5)')
    
    # Interactive command
    subparsers.add_parser('interactive', help='Interactive Q&A mode')
    
    # Clear command
    subparsers.add_parser('clear', help='Clear the vector index')
    
    # Status command
    subparsers.add_parser('status', help='Show index status')
    
    args = parser.parse_args()
    
    if args.command is None:
        parser.print_help()
        return 1
    
    # Route to appropriate command handler
    commands = {
        'ingest': cmd_ingest,
        'query': cmd_query,
        'interactive': cmd_interactive,
        'clear': cmd_clear,
        'status': cmd_status
    }
    
    try:
        return commands[args.command](args)
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        return 1
    except Exception as e:
        print(f"\nError: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
