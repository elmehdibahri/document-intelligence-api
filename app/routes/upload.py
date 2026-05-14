from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.chunker import chunk_text
from app.utils.embedder import store_chunks
import pdfplumber
import os

router = APIRouter()

UPLOAD_DIR = "uploads"

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Validate file type
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are accepted")
    
    # Save the file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)
    
    # Extract text
    extracted_text = ""
    page_count = 0
    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    
    if not extracted_text.strip():
        raise HTTPException(status_code=422, detail="Could not extract text from this PDF. It may be scanned or image-based.")
    
    # Chunk the text
    chunks = chunk_text(extracted_text, chunk_size=500, overlap=50)
    
    # Generate embeddings and store in ChromaDB
    storage_result = store_chunks(chunks, file.filename)
    
    return {
        "filename": file.filename,
        "page_count": page_count,
        "total_characters": len(extracted_text),
        "total_chunks": len(chunks),
        "embedding_dimensions": storage_result["embedding_dimensions"],
        "collection_name": storage_result["collection_name"],
        "message": f"Document processed and indexed. Ready for questions."
    }