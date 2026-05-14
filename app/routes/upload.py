from fastapi import APIRouter, UploadFile, File, HTTPException
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
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                extracted_text += text + "\n"
    
    # Return results
    return {
        "filename": file.filename,
        "pages": len(pdf.pages) if extracted_text else 0,
        "characters_extracted": len(extracted_text),
        "preview": extracted_text[:500]  # first 500 chars as preview
    }