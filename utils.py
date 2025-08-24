"""
Utility functions for data processing and embeddings
"""
from typing import List, Dict
import chromadb
from chromadb.utils import embedding_functions
from langchain.text_splitter import RecursiveCharacterTextSplitter

def create_embeddings_database() -> chromadb.Client:
    """Initialize ChromaDB client with sentence transformer embeddings"""
    client = chromadb.Client()
    return client

def process_documents(texts: List[str], chunk_size: int = 500) -> List[str]:
    """Split documents into chunks for processing"""
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=50,
        length_function=len,
    )
    chunks = text_splitter.create_documents(texts)
    return [chunk.page_content for chunk in chunks]

def create_nutrition_collection(client: chromadb.Client, documents: List[str], metadatas: List[Dict] = None):
    """Create and populate a collection with nutrition documents"""
    # Use sentence transformers for embeddings
    embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
        model_name="all-MiniLM-L6-v2"
    )
    
    # Create collection
    collection = client.create_collection(
        name="nutrition_docs",
        embedding_function=embedding_fn
    )
    
    # Add documents
    collection.add(
        documents=documents,
        ids=[f"doc_{i}" for i in range(len(documents))],
        metadatas=metadatas if metadatas else None
    )
    
    return collection
