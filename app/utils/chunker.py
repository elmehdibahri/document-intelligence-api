from typing import List

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[dict]:
    """
    Split text into overlapping chunks.
    
    Args:
        text: The full extracted text from a PDF
        chunk_size: How many characters per chunk (500 is a good default)
        overlap: How many characters to repeat between chunks (prevents losing context at boundaries)
    
    Returns:
        A list of dicts, each containing the chunk text and its position
    """
    if not text or len(text.strip()) == 0:
        return []
    
    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):
        # Define end of this chunk
        end = start + chunk_size
        
        # Extract the chunk
        chunk = text[start:end].strip()
        
        # Only add if chunk has meaningful content
        if len(chunk) > 20:
            chunks.append({
                "chunk_index": chunk_index,
                "text": chunk,
                "start_char": start,
                "end_char": end,
                "char_count": len(chunk)
            })
            chunk_index += 1
        
        # Move forward — but step back by overlap so chunks share some context
        start += chunk_size - overlap

    return chunks