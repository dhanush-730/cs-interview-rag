# Configuration settings for CS Interview RAG Assistant
import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    """Application configuration loaded from environment variables."""
    
    # Endee Vector Database Configuration
    endee_host: str = Field(
        default="http://localhost:8080",
        description="Endee server URL"
    )
    endee_auth_token: Optional[str] = Field(
        default=None,
        description="Optional auth token for Endee"
    )
    endee_index_name: str = Field(
        default="cs_interview_docs",
        description="Name of the vector index"
    )
    
    # Embedding Configuration
    embedding_model: str = Field(
        default="all-MiniLM-L6-v2",
        description="Sentence transformer model for embeddings"
    )
    embedding_dimension: int = Field(
        default=384,
        description="Dimension of embedding vectors"
    )
    
    # Chunking Configuration
    chunk_size: int = Field(
        default=1000,
        description="Number of characters per chunk"
    )
    chunk_overlap: int = Field(
        default=200,
        description="Number of overlapping characters between chunks"
    )
    
    # Retrieval Configuration
    top_k: int = Field(
        default=5,
        description="Number of chunks to retrieve"
    )
    
    # LLM Configuration
    google_api_key: Optional[str] = Field(
        default=None,
        description="Google API key for Gemini"
    )
    llm_model: str = Field(
        default="gemini-2.0-flash",
        description="LLM model to use"
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


# Global settings instance
settings = Settings()
