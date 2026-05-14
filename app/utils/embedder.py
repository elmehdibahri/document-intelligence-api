from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import os

# Load the embedding model once when the module loads
# This model runs locally — no API key needed
# It's small (90MB) but very capable for document search
model = SentenceTransformer('all-MiniLM-L6-v2')

# Set up ChromaDB — stores vectors in a local folder called 'vectorstore'
chroma_client = chromadb.PersistentClient(path="vectorstore")


def get_or_create_collection(collection_name: str):
    """Get existing collection or create a new one."""
    return chroma_client.get_or_create_collection(
        name=collection_name,
        metadata={"hnsw:space": "cosine"}  # use cosine similarity for search
    )


def store_chunks(chunks: list, document_name: str) -> dict:
    """
    Convert text chunks to vectors and store them in ChromaDB.
    
    Args:
        chunks: List of chunk dicts from our chunker
        document_name: Used as the collection name
    
    Returns:
        Summary of what was stored
    """
    # Sanitise collection name — ChromaDB doesn't like spaces or dots
    collection_name = document_name.replace(" ", "_").replace(".", "_").lower()
    
    collection = get_or_create_collection(collection_name)
    
    # Extract just the text from each chunk
    texts = [chunk["text"] for chunk in chunks]
    
    # Generate embeddings for all chunks at once (faster than one at a time)
    print(f"Generating embeddings for {len(texts)} chunks...")
    embeddings = model.encode(texts).tolist()
    
    # Create unique IDs for each chunk
    ids = [f"{collection_name}_chunk_{chunk['chunk_index']}" for chunk in chunks]
    
    # Store in ChromaDB — text, embedding, and metadata together
    collection.upsert(
        ids=ids,
        embeddings=embeddings,
        documents=texts,
        metadatas=[{
            "chunk_index": chunk["chunk_index"],
            "start_char": chunk["start_char"],
            "end_char": chunk["end_char"],
            "document": document_name
        } for chunk in chunks]
    )
    
    return {
        "collection_name": collection_name,
        "chunks_stored": len(chunks),
        "embedding_dimensions": len(embeddings[0])
    }


def search_chunks(query: str, document_name: str, top_k: int = 3) -> list:
    """
    Search for the most relevant chunks for a given query.
    
    Args:
        query: The user's question
        document_name: Which document to search in
        top_k: How many chunks to return
    
    Returns:
        List of the most relevant chunks
    """
    collection_name = document_name.replace(" ", "_").replace(".", "_").lower()
    
    try:
        collection = chroma_client.get_collection(collection_name)
    except Exception:
        return []
    
    # Convert the question to a vector
    query_embedding = model.encode([query]).tolist()
    
    # Find the most similar chunks
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=min(top_k, collection.count())
    )
    
    # Format the results cleanly
    relevant_chunks = []
    for i, doc in enumerate(results["documents"][0]):
        relevant_chunks.append({
            "text": doc,
            "relevance_score": round(1 - results["distances"][0][i], 4),
            "metadata": results["metadatas"][0][i]
        })
    
    return relevant_chunks