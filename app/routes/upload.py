from fastapi import APIRouter, UploadFile, File, HTTPException
from app.utils.chunker import chunk_text
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
    
    # Extract text page by page
    extracted_text = ""
    page_count = 0

    with pdfplumber.open(file_path) as pdf:
        page_count = len(pdf.pages)
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    
    # Chunk the extracted text
    chunks = chunk_text(extracted_text, chunk_size=500, overlap=50)

    # Return results
    return {
        "filename": file.filename,
        "page_count": page_count,
        "total_characters": len(extracted_text),
        "total_chunks": len(chunks),
        "chunks": chunks[:3],  # Only return first 3 chunks in the response (preview)
        "message": f"Successfully processed {page_count} pages into {len(chunks)} chunks"
    }